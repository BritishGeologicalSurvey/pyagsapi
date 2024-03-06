"""
Functions used to generate a map of borehole locations by extracting a GeoJSON
representation of their metadata from the AGS files.
"""
import json
import logging
from pathlib import Path

import pandas as pd
import geopandas as gpd

from app.checkers import load_tables_reporting_errors
from app.bgs_rules import create_location_gpd

logger = logging.getLogger(__name__)


def extract_geojson(filepath: Path) -> dict:
    """
    Read an AGS4 file and extract geojson represenation of LOCA table and
    metadata. 
    """
    logger.info("Extracting geojson from  %s", filepath.name)

    # Read data file
    tables, load_error, _ = load_tables_reporting_errors(filepath)
    if load_error:
        raise ValueError(load_error)

    # Convert to geodataframe
    try:
        location: gpd.GeoDataFrame = create_location_gpd(tables)
    except KeyError:
        msg = f"ERROR: LOCA group missing from {filepath}"
        raise ValueError(msg)
    
    # Add project columns and drop unwanted columns
    try:
        project: pd.DataFrame = tables['PROJ']
    except KeyError:
        msg = f"ERROR: PROJ group missing from {filepath}"
        raise ValueError(msg)

    for column in project.columns:
        if column.startswith('PROJ_'):
            # We assume that each file contains just one project
            location[column] = project.loc[0, column]

    try:
        location['PROJ_FILE_FSET'] = project.loc[0, 'FILE_FSET']
        location.rename(columns={'FILE_FSET': 'LOCA_FILE_FSET'}, inplace=True)
    except KeyError:
        logger.debug("No FILE_FSET for either/both PROJ and LOCA groups for %s",
                     filepath)
    del location['HEADING']

    # Create new ID from project and location IDs
    location.reset_index(inplace=True)
    location['ID'] = location['PROJ_ID'].str.cat(location['LOCA_ID'], sep='.')
    location.set_index('ID', inplace=True)

    # Reproject to WGS84
    location = location.to_crs('EPSG:4326')
    
    # Return dict representation of geojson
    return json.loads(location.to_json())
