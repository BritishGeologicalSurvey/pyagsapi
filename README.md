# AGS Application

An application using the AGS Python library to:

- Validate AGS files
- Convert AGS files
- Provide API to also do the above. 

## Installation 

### Docker

Docker image based on: 

- uvicorn
- gunicorn
- fastapi

Build your image

```bash
docker build -t myimage .
```
Run a container based on your image:

```bash
docker run -d --name mycontainer -p 80:80 myimage
```

See detailed docs at https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
