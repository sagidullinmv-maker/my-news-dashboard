FROM python:3.11-slim

WORKDIR /app

# Копируем все файлы
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Проверяем установку
RUN pip list | grep gunicorn

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
