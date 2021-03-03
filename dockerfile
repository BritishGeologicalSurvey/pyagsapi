FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

## Install python-ags4

RUN pip install python-ags4

## Test Installation

RUN ags4_cli check --help

## To allow file uploads

RUN pip install python-multipart

COPY ./app /app

