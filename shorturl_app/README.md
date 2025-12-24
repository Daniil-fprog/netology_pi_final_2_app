=== Старт локально ===
cd todo_app
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001


=== Старт через Docker ===
# 1. Соберите образ (из корня проекта, где лежит Dockerfile)
docker build -t shorturl-service .

# 2. Создайте именованный том (если ещё не создан)
docker volume create shorturl_data

# 3. Запустите контейнер
docker run -d \
  --name shorturl-app \
  -p 8001:80 \
  -v shorturl_data:/app/data \
  shorturl-service
