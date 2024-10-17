FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . ./app/

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"]
