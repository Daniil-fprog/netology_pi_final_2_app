=== Старт локально ===
cd todo_app
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000


=== Старт через Docker ===
# 1. Соберите образ (из корня проекта, где лежит Dockerfile)
docker build -t todo-service .

# 2. Создайте именованный том (если ещё не создан)
docker volume create todo_data

# 3. Запустите контейнер
docker run -d \
  --name todo-app \
  -p 8000:80 \
  -v todo_data:/app/data \
  todo-service