FROM python:3.13.5-alpine3.22

## Install python-ags4
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN rm -rf /app/*
COPY ./app /app/app

EXPOSE 80
CMD [ "fastapi", "run", "app/main.py", "--port", "80" ]
