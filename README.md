# AGS Utilities

HTTP API for the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library).

It can:

- Validate AGS files to v4.x of the AGS data format standard
- Convert between AGS format files and spreadsheets files `.ags` <-> `.xlsx`

Additionally .ags files can be validated for submission to the [National Geoscience Data Center (NGDC)](http://transfer.bgs.ac.uk/ingestion)


## Documentation 

Read the docs at https://britishgeologicalsurvey.github.io/AGS-Validator/ for full documentation.


## Quick start

The simplest way to run the validation service is via Docker:

```
docker run -p 80:80 --name ags-validator ghcr.io/britishgeologicalsurvey/ags_utilities
```

Navigate to [http://localhost](http://localhost) to see the landing page or
[http://localhost/docs](http://localhost/docs) to see the API documentation via
the Swagger interface.

The `latest` tag reflects the current state of the `main` branch of the
repository.
See
[Releases](https://github.com/BritishGeologicalSurvey/AGS-Validator/releases)
for details of other versions.


## Development

### Running locally

AGS Validator is written in Python and based on the
[FastAPI](https://fastapi.tiangolo.com/) framework.
It runs on the [Uvicorn](https://www.uvicorn.org/) ASGI server.

Use the following commands to run the API locally:

```bash
git clone https://github.com/BritishGeologicalSurvey/AGS-validator
cd AGS-validator
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default, the API is served at
[http://localhost:8000](http://localhost:8000).

### Running tests

Use the following to run the tests:

```bash
pip install -r requirements_dev.txt
export PYTHONPATH=.
pytest -vs test
```

The test environment is configured so that adding `--pdb` to the test command
will start an IPython debugger session in the event of test failure.


### Licence

`AGS Validator` was created by and is maintained by the British Geological Survey.
It is distributed under the [LGPL v3.0 licence](LICENSE).
Copyright: © BGS / UKRI 2021
