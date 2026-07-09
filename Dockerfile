FROM python:3.13.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./


RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

ENV PYTHONPATH=/app

CMD alembic upgrade head; python src/main.py