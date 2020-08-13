FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY alembic.ini ./alembic.ini
COPY alembic /app/alembic
COPY ./app ./app
