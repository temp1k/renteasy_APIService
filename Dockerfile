# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную окружения PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем зависимости
COPY requirements.txt /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта в рабочую директорию
COPY . /code/

# Определяем переменные окружения для подключения к базе данных PostgreSQL
ENV POSTGRES_DB='renteasy_db'
ENV POSTGRES_USER='renteasy_admin'
ENV POSTGRES_PASSWORD='P@ssw0rd'
ENV POSTGRES_HOST='127.0.0.1'
ENV POSTGRES_PORT='5432'

# Запускаем приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
