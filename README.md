# pyagsapi - AGS File Utilities API

![GitHub release (latest by date)](https://img.shields.io/github/v/release/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/BritishGeologicalSurvey/pyagsapi/lint_and_test.yml?label=Tests&style=for-the-badge)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/BritishGeologicalSurvey/pyagsapi/main.yml?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub commits since tagged version](https://img.shields.io/github/commits-since/BritishGeologicalSurvey/pyagsapi/v7.0?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/BritishGeologicalSurvey/pyagsapi?style=for-the-badge)

A HTTP API for the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library), built on the [FastAPI](https://fastapi.tiangolo.com/) framework and served via the [Uvicorn](https://www.uvicorn.org/) ASGI server.

It can:

- Validate AGS files to v4.x of the AGS data format standard
- Validate AGS files for submission to the [National Geoscience Data Center (NGDC)](https://transfer.bgs.ac.uk/ingestion)
- Extract geojson from submitted files and plot on a map
- Convert between AGS format files and spreadsheet files `.ags` <-> `.xlsx`
- Download PDF logs of existing files within the National Geoscience Data Centre

The core Python API provides the functionality to validate and convert AGS geotechnical data. From here, standard Python web frameworks like Uvicorn and Starlette provide the web API/wrapper atop the core Python API.

BGS Deployed Instance available at: [https://agsapi.bgs.ac.uk/](https://agsapi.bgs.ac.uk/)

## Quick start

### Docker

The simplest way to run the validation service is via Docker:
docker run -p 8000:8000 --name pyagsapi ghcr.io/britishgeologicalsurvey/pyagsapi:latest

Navigate to [http://localhost:8000](http://localhost:8000) to see the landing page or [http://localhost:8000/docs](http://localhost:8000/docs) to see the API documentation via the Swagger interface.

The `latest` tag reflects the current state of the `main` branch of the repository. It may have breaking changes. Use versions from tagged [Releases](https://github.com/BritishGeologicalSurvey/pyagsapi/releases) to fix the version in deployment pipelines. Available tags are listed in the [Container Registry](https://github.com/BritishGeologicalSurvey/pyagsapi/pkgs/container/pyagsapi).

### Setting the `root_path`

If you are running behind a proxy, you may need to set the `root_path` using the `PYAGSAPI_ROOT_PATH` environment variable:
docker run -p 8000:8000 -e PYAGSAPI_ROOT_PATH="/pyagsapi" --name pyagsapi ghcr.io/britishgeologicalsurvey/pyagsapi

This will ensure that all references to `self` in responses, and all Swagger and REDOC documentation, include the correct path.

### From Source

pyagsapi targets Python >= 3.13.

```bash
python -m venv pyagsapi
source pyagsapi/bin/activate
git clone https://github.com/BritishGeologicalSurvey/pyagsapi.git
cd pyagsapi
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be served at [http://localhost:8000](http://localhost:8000).

## Development

The main repo for this project is [https://github.com/BritishGeologicalSurvey/pyagsapi/](https://github.com/BritishGeologicalSurvey/pyagsapi/).

Please raise any feature requests, issues or pull requests against this repository.

### Running tests

Use the following to run the tests:

```bash
pip install -r requirements_dev.txt
export PYTHONPATH=.
pytest -vs test
```

The test environment is configured so that adding `--pdb` to the test command will start an IPython debugger session in the event of test failure.

### Updating dependencies

We are using [pip-tools](https://pip-tools.readthedocs.io/en/stable/) to create a pinned list of all dependencies from the ones that we need to specify.

To refresh the dependency list, update `requirements.in` and `requirements-dev.in` then run the following:

```bash
pip-compile -o requirements.txt requirements.in
pip-compile -o requirements_dev.txt requirements_dev.in
```

The updated requirements files must be edited to remove reference to the Nexus mirror before they can then be committed.

### GUI Customisation

To amend the GUI HTML we recommend running via `Docker` using your own `Dockerfile` like the below to `COPY` in your own templates.
FROM ghcr.io/britishgeologicalsurvey/pyagsapi:7.0
COPY content/static /code/app/static
COPY content/templates /code/app/templates

## Releasing

Before tagging a new release, update **all** of the following so the version reported by the API, the git tag, and the published container image agree:

- [ ] `app/version.py` — bump `API_VERSION` to the new version
- [ ] Update any version-specific examples in `README.md` (the `GUI Customisation` Dockerfile example pins a version)
- [ ] Commit and push the above to `main`
- [ ] Tag the release: `git tag vX.Y && git push origin vX.Y`
- [ ] Confirm the GitHub Actions workflow publishes the matching `ghcr.io/britishgeologicalsurvey/pyagsapi:X.Y` image
- [ ] Verify the running image reports the new version at `/api` (or whichever endpoint surfaces `API_VERSION`)

## Container Registry

Containers for the application are hosted in the GitHub Container Registry.

Every push to `main` branch commits builds `pyagsapi:latest`.

Tagged releases matching `v?<major>.<minor>(.<patch>)?` build images with the `v` stripped from the tag — e.g. tagging `v2.0` builds `pyagsapi:2.0`.

Release candidates matching `v?<major>.<minor>(.<patch>)?-rc` build images with the same name — e.g. tagging `v3.1.1-rc` builds `pyagsapi:3.1.1-rc`.

## Example Files

Files in [https://github.com/BritishGeologicalSurvey/pyagsapi/tree/main/test/files/real](https://github.com/BritishGeologicalSurvey/pyagsapi/tree/main/test/files/real) are a collection of real AGS files which have been submitted to the BGS and are available under OGL, we have included them here as example files for testing pyagsapi.

## Licence

`pyagsapi` was created by and is maintained by the British Geological Survey.
It is distributed under the [LGPL v3.0 licence](LICENSE).
Copyright: © BGS / UKRI 2021–2026

Contains data supplied by Natural Environment Research Council.

Contains public sector information licensed under the Open Government Licence v3.0