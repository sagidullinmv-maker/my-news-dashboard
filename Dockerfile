FROM python:3.11-slim

WORKDIR /app

# Копируем всё
COPY . .

# Только устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Просто смотрим, что в папке
RUN ls -la /app && \
    echo "=== Поиск app.py ===" && \
    find /app -name "app.py" || echo "app.py не найден"

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
