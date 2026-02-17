FROM python:3.11-slim

WORKDIR /app

# Явно копируем основные файлы
COPY app.py .
COPY requirements.txt .
COPY templates/ ./templates/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Проверяем, что файлы на месте
RUN ls -la /app && ls -la /app/templates/

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
