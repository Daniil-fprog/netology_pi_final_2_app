from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import TodoItem
from .schemas import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(title="ToDo-сервис")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/items", response_model=TodoResponse)
def create_item(item: TodoCreate, db: Session = Depends(get_db)):
    todo = TodoItem(**item.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/items", response_model=list[TodoResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(TodoItem).all()

@app.get("/items/{item_id}", response_model=TodoResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=TodoResponse)
def update_item(item_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    item = db.query(TodoItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
        
    db.commit()
    db.refresh(item)
    return item

    
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()