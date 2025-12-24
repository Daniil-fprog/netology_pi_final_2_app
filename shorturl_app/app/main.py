from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import UrlModel
from .schemas import UrlCreate, UrlResponse

app = FastAPI(title="Short URL Service")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def make_short_url(short_id: int):
    return f"http://localhost:8001/{short_id}"

# POST /shorten
@app.post("/shorten", response_model=UrlResponse)
def shorten_url(data: UrlCreate, db: Session = Depends(get_db)):
    item = UrlModel(full_url=str(data.url))
    db.add(item)
    db.commit()
    db.refresh(item)

    return UrlResponse(
        short_id=item.id,
        full_url=item.full_url,
        short_url=make_short_url(item.id)
    )

# GET /{short_id}
@app.get("/{short_id}")
def redirect(short_id: int, db: Session = Depends(get_db)):
    item = db.query(UrlModel).get(short_id)
    if not item:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(item.full_url)

# GET /stats/{short_id}
@app.get("/stats/{short_id}", response_model=UrlResponse)
def stats(short_id: int, db: Session = Depends(get_db)):
    item = db.query(UrlModel).get(short_id)
    if not item:
        raise HTTPException(status_code=404, detail="URL not found")

    return UrlResponse(
        short_id=item.id,
        full_url=item.full_url,
        short_url=make_short_url(item.id)
    )
