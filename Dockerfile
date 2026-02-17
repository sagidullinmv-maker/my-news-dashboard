FROM python:3.11-slim

WORKDIR /app

# Копируем всё сразу (так проще и надёжнее)
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт
EXPOSE 80

# Запускаем приложение
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
