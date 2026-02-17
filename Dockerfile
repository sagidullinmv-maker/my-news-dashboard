FROM python:3.11-slim

WORKDIR /app

# Копируем всё
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем текущую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# Проверяем, что app.py виден
RUN python -c "import sys; print('Python path:', sys.path); import app; print('✅ app.py импортирован успешно')"

EXPOSE 80

# Запускаем с явным указанием директории
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--chdir", "/app", "app:app"]
