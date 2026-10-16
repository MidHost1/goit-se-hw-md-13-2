# Вибираємо базовий образ Python 3.13
FROM python:3.13-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Встановлюємо системні залежності, необхідні для збірки деяких пакетів (наприклад, для psycopg2/Postgres)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Копіюємо файл залежностей Poetry
COPY pyproject.toml poetry.lock ./

# Встановлюємо Python-залежності через Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Копіюємо весь решту коду проєкту у контейнер
COPY . .

# Відкриваємо порт для сервера
EXPOSE 8000