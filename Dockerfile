FROM python:3.11-slim

WORKDIR /app

# Копируем всё (так проще и надёжнее)
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Проверяем, что файлы на месте
RUN ls -la /app && echo "✅ Файлы скопированы"

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
