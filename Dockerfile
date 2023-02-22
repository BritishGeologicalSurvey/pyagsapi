FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-2021-10-02

## Install python-ags4
COPY requirements.txt .
RUN pip install -r requirements.txt


RUN rm -rf /app/*
COPY ./app /app/app
