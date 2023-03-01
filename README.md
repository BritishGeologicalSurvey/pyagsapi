# pyagsapi - AGS File Utilities API

A HTTP API for the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library).

It can:

- Validate AGS files to v4.x of the AGS data format standard
- Convert between AGS format files and spreadsheet files `.ags` <-> `.xlsx`

Additionally .ags files can be validated for submission to the [National Geoscience Data Center (NGDC)](http://transfer.bgs.ac.uk/ingestion)

It is built on the FastAPI framework, using the official FastAPI docker image as it's base.

The core Python API provides the functionality to validate and convert AGS geotechnical data. From here, standard Python web frameworks like Uvicorn and Starlette provide the web API/wrapper atop the core Python API.

## Quick start

### Docker

The simplest way to run the validation service is via Docker:

```
docker run -p 80:80 --name pyagsapi ghcr.io/britishgeologicalsurvey/pyagsapi:latest
```

Navigate to [http://localhost](http://localhost) to see the landing page or [http://localhost/docs](http://localhost/docs) to see the API documentation via the Swagger interface.

The `latest` tag reflects the current state of the `main` branch of the repository. It may have breaking changes. Use versions from tagged [Releases](https://github.com/BritishGeologicalSurvey/pyagsapi/releases) to fix the version in deployment pipelines. Available tags are listed in the [Container Registry](https://github.com/BritishGeologicalSurvey/AGS-Validator/pkgs/container/pyagsapi).

### Setting the `root_path`

If you are running behind a proxy, you may need to set the `root_path` using the `PYAGSAPI_ROOT_PATH` environment variable:

```
docker run -p 80:80 -e PYAGSAPI_ROOT_PATH="/pyagsapi" --name pyagsapi ghcr.io/britishgeologicalsurvey/pyagsapi
```

This will ensure that all references to `self` in responses, and all Swagger and REDOC documentation, include the correct path.

### From Source

pyagsapi runs on Python 3.

```python
python -m venv pyagsapi
cd pyagsapi
. bin/activate
git clone https://github.com/BritishGeologicalSurvey/pyagsapi.git
cd pyagsapi
pip install -r requirements.txt
uvicorn app.main:app 
```

## Development

The main repo for this project is [https://github.com/BritishGeologicalSurvey/pyagsapi/](https://github.com/BritishGeologicalSurvey/pyagsapi/).

Please raise any feature requests, issues or pull requests against this repository.

### Running locally

AGS Validator is written in Python and based on the [FastAPI](https://fastapi.tiangolo.com/) framework. It runs on the [Uvicorn](https://www.uvicorn.org/) ASGI server.

Use the following commands to run the API locally:

```bash
git clone https://github.com/BritishGeologicalSurvey/pyagsapi
cd pyagsapi
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default, the API is served at [http://localhost:8000](http://localhost:8000).

### Running tests

Use the following to run the tests:

```bash
pip install -r requirements_dev.txt
export PYTHONPATH=.
pytest -vs test
```

The test environment is configured so that adding `--pdb` to the test command will start an IPython debugger session in the event of test failure.

### GUI Customisation

To ammend the GUI HTML we recommend running via `Docker` using your own `Dockerfile` like the below to `COPY` in your own templates.

```
FROM ghcr.io/britishgeologicalsurvey/pyagsapi:2.0

COPY content/static /app/app/static
COPY content/templates /app/app/templates
```

### Container Registry

Containers for the application are hosted in the GitHub Container Registry

Every push to `Main` branch commits builds `pyagsapi:latest`.

Push Tagged Releases with `^v?[0-9]+[.][0-9]+([.][0-9])?` (v* == v2.0) builds `pyagsapi:2.0` (the "v" gets dropped for the tag).

You can also push release candidates using the format `/^v?[0-9]+[.][0-9]+([.][0-9])?\-rc/` e.g. v3.1.1-rc builds `pyagsapi:3.1.1-rc`

### Example Files

Files in [https://github.com/BritishGeologicalSurvey/pyagsapi/tree/main/test/files/real](https://github.com/BritishGeologicalSurvey/pyagsapi/tree/main/test/files/real) are a random collection of real AGS files which have been submitted to the BGS and are available under OGL, we have included them here as example files for testing pyagsapi.

## Licence

`pyagsapi` was created by and is maintained by the British Geological Survey.
It is distributed under the [LGPL v3.0 licence](LICENSE).
Copyright: © BGS / UKRI 2021

Contains data supplied by Natural Environment Research Council.

Contains public sector information licensed under the Open Government Licence v3.0
