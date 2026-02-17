FROM python:3.11-slim

WORKDIR /app

# Копируем только requirements.txt сначала (для кэширования)
COPY requirements.txt .

# Устанавливаем зависимости с подробным выводом
RUN pip install --no-cache-dir -v -r requirements.txt

# Копируем остальные файлы
COPY . .

# Проверяем, что gunicorn установился
RUN which gunicorn && echo "✅ Gunicorn installed" || echo "❌ Gunicorn NOT found"

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
