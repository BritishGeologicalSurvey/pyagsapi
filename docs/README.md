# AGS Utilities

## Introduction

BGS AGS Utilities App offers a FastAPI implementation of the [AGS Python library](https://gitlab.com/ags-data-format-wg/ags-python-library) to:

- Validate AGS files to v4.x of the AGS data format standard. 
- Convert AGS files .ags<>.xlsx

## Future Features 

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


## Deployment

### Locally

Setup your python virtutal environment then 

```bash
uvicorn app.main:app --reload
```

### Docker 

Container packages are published to GitHub, main branch is tagged `latest`, tagged releases use their version number `1,0-alpha` 


```bash
docker run -d --name mycontainer -p 80:80 ghcr.io/britishgeologicalsurvey/ags_utilities:latest
```

## Have a specific question?

* Use the search bar in the top left to search this documentation
* Check the [FAQ section](other/faq)

## Have an issue?

Raise an issue on GitHub [Issue Tracker](https://github.com/BritishGeologicalSurvey/AGS-Validator/issues) 


## Documenting the Documentation

This documentation is written in Markdown built & hosted on GitHub
pages, built using [Docsify](https://docsify.js.org).



