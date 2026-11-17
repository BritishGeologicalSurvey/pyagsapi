FROM python:3.13.5-slim

# Create a non-root user with a known UID for k8s securityContext.runAsUser
RUN groupadd -g 1000 -r appgroup \
 && useradd  -u 1000 -r -g appgroup -d /code -s /sbin/nologin appuser

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Ensure /app directory is owned by root so it cannot be written to by appuser
COPY ./app /code/app

USER appuser

EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]