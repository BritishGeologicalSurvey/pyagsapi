FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

## Install python-ags4
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app/app

