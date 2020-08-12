FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY alembic.ini .
COPY ./alembic .

RUN alembic upgrade head

COPY ./app .
