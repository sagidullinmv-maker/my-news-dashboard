FROM python:3.11-slim

WORKDIR /app

# Копируем всё, игнорируя .gitignore
COPY --chown=root:root . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Подробная проверка
RUN echo "=== ВСЕ ФАЙЛЫ ===" && ls -la /app && \
    echo "=== ПОИСК APP.PY ===" && find /app -name "app.py" || echo "❌ app.py НЕ НАЙДЕН"

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
