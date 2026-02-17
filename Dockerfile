# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости (включая gunicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Указываем порт, который слушает приложение
EXPOSE 80

# Команда для запуска через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
