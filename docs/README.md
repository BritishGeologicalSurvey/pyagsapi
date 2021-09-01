# pyagsapi - AGS File Validation and Conversion

## Introduction

BGS pyagsapi offers a FastAPI implementation of the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library). 

## Features

- Validate AGS files to v4.x of the AGS data format standard. 
- Convert AGS files .ags<-->.xlsx

### Future Features 

Additionally .ags files can be validated for submission to the [National Geoscience Data Center (NGDC)](http://transfer.bgs.ac.uk/ingestion)

This will check: 

- Basic formatting: number of columns must match number of column headers
- Groups must include PROJ, LOCA or HOLE, ABBR, TYPE, UNITS (and GEOL for BGS)
- FILE is required if the AGS file is submitted with other supporting non-AGS files
- DICT is required if any user defined groups or headings are present, otherwise only standard/default settings are used
- LOCA/HOLE file must contain a minimum of 75 per cent valid coordinates
- The spatial referencing sytem or projection format should be specified in LOCA_GREF, LOCA_LREF or LOCA_LLZ columns (or HOLE equivalent)
- OSGB coordinates should be in the LOCA_NATE and LOCA_NATN columns(or HOLE equivalent)
- Local grid reference coordinates should be in the LOCA_LOCX and LOCA_LOCY columns(or HOLE equivalent)
- LAT/LON coordinates should be in the LOCA_LAT and LOCA_LON columns(or HOLE equivalent)
- Local coordinates should not be duplicated in the BNG columns as this would indicate they have not been converted

## How pyagsapi Works

pyagsapi is a python-based http server implementation of the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library). 

It is built on the FastAPI framework, using the official FastAPI docker image as it's base.

The core Python API provides the functionality to validate and convert AGS geotechnical data. From here, standard Python web frameworks like Uvicorn and Starlette provide the web API/wrapper atop the core Python API.

## Install

pyagsapi is easy to install on numerous environments.

### Requirements & Dependencies

pyagsapi runs on Python 3. 

### From Source

```python
python -m venv pyagsapi
cd pyagsapi
. bin/activate
git clone https://github.com/BritishGeologicalSurvey/pyagsapi.git
cd pyagsapi
pip install -r requirements.txt
uvicorn app.main:app 
```

### Docker 

Container packages are published to GitHub, main branch is tagged `latest`, tagged releases use their version number `1,0-alpha` 

[Container Registry](https://github.com/BritishGeologicalSurvey/AGS-Validator/pkgs/container/pyagsapi)


```bash
docker run -d --name mycontainer -p 80:80 ghcr.io/britishgeologicalsurvey/pyagsapi:latest
```

## Configuration

### GUI

To ammend the GUI HTML we recommend running via `Docker` using your own `Dockerfile` like the below. 

```
FROM ghcr.io/britishgeologicalsurvey/pyagsapi:2.0

COPY content/static /app/app/static
COPY content/templates /app/app/templates
```

Example HTML can be found in the `example-html` folder. 

## Deployment

### Docker

pyagsapi provides an official Docker image which is made available on the GitHub Container Registry. 

#### The Basics

The official pyagsapi Docker image will start a pyagsapi Docker container using FastAPI on internal port 80.

To run :

```
docker run -d --name mycontainer -p 80:80 ghcr.io/britishgeologicalsurvey/pyagsapi:latest
```
## Development

The main repo for this project is https://github.com/BritishGeologicalSurvey/pyagsapi/. 

Please raise any feature requests, issues or pull requests against this repository.

### Container Registry

Containers for the application are hosted in the GitHub Container Registry  

Every push to `Main` branch commits builds `pyagsapi:latest`
Pushed Tagged Releases with v* (v* == v2.0) builds `pyagsapi:2.0` (the "v" gets dropped for the tag)

> Making tagged release via the GitHub.com gui does not build a container, developers need to create a tag locally then `git push origin v0.1.0-test`

## Have a specific question?

* Use the search bar in the top left to search this documentation

## Have an issue?

Raise an issue on GitHub [Issue Tracker](https://github.com/BritishGeologicalSurvey/pyagsapi/issues) 


## Documenting the Documentation

This documentation is written in Markdown built & hosted on GitHub
pages, built using [Docsify](https://docsify.js.org).