FROM python:3.13.5-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 80
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
