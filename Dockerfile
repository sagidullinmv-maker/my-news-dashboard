FROM python:3.11-slim

WORKDIR /app

# Копируем всё
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем текущую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# ПОДРОБНАЯ ПРОВЕРКА
RUN ls -la /app && \
    echo "=== СОДЕРЖИМОЕ ПАПКИ /app ===" && \
    find /app -name "*.py" -type f | head -20 && \
    echo "=== ПРОВЕРКА ИМПОРТА ===" && \
    python -c "import sys; print('Python path:', sys.path); import app; print('✅ app.py импортирован успешно')" || \
    (echo "❌ ОШИБКА: app.py не найден или не импортируется" && exit 1)

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--chdir", "/app", "app:app"]
