"""Functions for each of the BGS data validation rules"""
from pathlib import Path
from typing import List

from shapely.geometry import Point
from pyproj.transformer import Transformer
import geopandas as gpd

"""
The gb_outline.geojson file contains public sector information licensed under
Open Government Licence v3.0.  It was generated from Ordnance Survey Open Data
via the following commands:

import geopandas as gpd
gb_outline = gpd.read_file('app/country_outlines.gpkg', layer='gb_outline')
simple = gb_outline.geometry.simplify(100, preserve_topology=False)
buffer = simple.buffer(1000)
simple_buffer = buffer.simplify(1000)
with open('app/gb_outline.geojson', 'wt') as outfile:
    outfile.write(simple_buffer.to_json())
"""


GB_OUTLINE = Path(__file__).parent / 'gb_outline.geojson'
NI_OUTLINE = Path(__file__).parent / 'ni_outline.geojson'
bgs_rules_version = '2.0.0'


def check_required_groups(tables: dict) -> List[dict]:
    """ Groups must include PROJ, LOCA or HOLE, ABBR, TYPE, UNIT """
    errors = []
    required = ['PROJ', 'ABBR', 'TYPE', 'UNIT']
    missing = []

    for group in required:
        if group not in tables.keys():
            missing.append(group)

    if 'LOCA' not in tables.keys() and 'HOLE' not in tables.keys():
        missing.append('(LOCA or HOLE)')

    if missing:
        desc = 'Required groups not present: ' + ', '.join(missing)
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


def check_required_bgs_groups(tables: dict) -> List[dict]:
    """ Groups must include GEOL for BGS """
    errors = []
    required = ['GEOL']
    missing = []

    for group in required:
        if group not in tables.keys():
            missing.append(group)

    if missing:
        desc = 'Required BGS groups not present: ' + ', '.join(missing)
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


def check_spatial_referencing_system(tables: dict) -> List[dict]:
    """ Spatial referencing system defined in LOCA_GREF, LOCA_LREF or LOCA_LLZ """
    ref_found = False
    errors = []

    try:
        location = tables['LOCA']
        for col in ['LOCA_GREF', 'LOCA_LREF', 'LOCA_LLZ']:
            try:
                if all(location[col] != ''):
                    ref_found = True
            except KeyError:
                pass
        if not ref_found:
            desc = 'Spatial referencing system not in LOCA_GREF, LOCA_LREF or LOCA_LLZ!'
            errors.append({'line': '-', 'group': 'LOCA', 'desc': desc})
    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_eastings_northings_present(tables: dict) -> List[dict]:
    """Eastings and Northings columns are populated"""
    errors = []
    try:
        location = tables['LOCA']
        if any(location['LOCA_NATE'].isna()) or any(location['LOCA_NATE'] == 0):
            errors.append(
                {'line': '-', 'group': 'LOCA',
                 'desc': 'LOCA_NATE contains zeros or null values'})
        if any(location['LOCA_NATN'].isna()) or any(location['LOCA_NATN'] == 0):
            errors.append(
                {'line': '-', 'group': 'LOCA',
                 'desc': 'LOCA_NATN contains zeros or null values'})
    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_eastings_northings_range(tables: dict) -> List[dict]:
    """Eastings and Northings columns fall within reasonable range"""
    errors = []
    try:
        location = tables['LOCA']
        if any(location['LOCA_NATE'] < 1e5) or any(location['LOCA_NATE'] > 8e5):
            errors.append(
                {'line': '-', 'group': 'LOCA',
                 'desc': 'LOCA_NATE values outside 100,000 to 800,000 range'})
        if any(location['LOCA_NATN'] < 1e5) or any(location['LOCA_NATN'] > 1.4e6):
            errors.append(
                {'line': '-', 'group': 'LOCA',
                 'desc': 'LOCA_NATN values outside 100,000 to 1,400,000 range'})
    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_drill_depth_present(tables: dict) -> List[dict]:
    """Drill depth value is populate and not zero"""
    errors = []
    try:
        depth = tables['HDPH']
        if any(depth['HDPH_TOP'].isna()):
            errors.append(
                {'line': '-', 'group': 'HDPH',
                 'desc': 'HDPH_TOP contains null values'})
        if any(depth['HDPH_BASE'].isna()) or any(depth['HDPH_BASE'] == 0):
            errors.append(
                {'line': '-', 'group': 'HDPH',
                 'desc': 'HDPH_BASE contains zero or null values'})
    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_drill_depth_geol_record(tables: dict) -> List[dict]:
    """Drill depths have corresponding records in geol table"""
    errors = []
    try:
        depth = tables['HDPH']
        geology = tables['GEOL']
        geology_ids = set(geology['LOCA_ID'].unique())
        depth_ids = set(depth['LOCA_ID'].unique())

        if not_in_geology := depth_ids.difference(geology_ids):
            errors.append(
                {'line': '-', 'group': 'HDPH',
                 'desc': f'HDPH LOCA_IDs not in GEOL group ({not_in_geology})'})
        if not_in_depth := geology_ids.difference(depth_ids):
            errors.append(
                {'line': '-', 'group': 'HDPH',
                 'desc': f'GEOL LOCA_IDs not in HDPH group ({not_in_depth})'})

    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_loca_within_great_britain(tables: dict) -> List[dict]:
    """Location coordinates fall on land within Great Britain."""
    errors = []

    def check_coordinates(row):
        """Return errors for rows that are outside polygons."""
        gb_outline = gpd.read_file(GB_OUTLINE).loc[0, 'geometry']
        ni_outline = gpd.read_file(NI_OUTLINE).loc[0, 'geometry']
        to_irish_grid = Transformer.from_crs("EPSG:27700", "EPSG:29903", always_xy=True)

        # Check for points within gb_outline
        if row['geometry'].intersects(gb_outline):
            return None

        # Check if points outside gb_outline are in ni_outline
        ni_grid_geometry = Point(to_irish_grid.transform(row['geometry'].x, row['geometry'].y))
        if ni_grid_geometry.intersects(ni_outline):
            if row['LOCA_GREF']:
                return None
            else:
                return {'line': '-', 'group': 'LOCA',
                        'desc': f'NATE / NATN in Northern Ireland but LOCA_GREF undefined ({row.name})'}

        # Otherwise return error
        return {'line': '-', 'group': 'LOCA',
                'desc': f'NATE / NATN outside Great Britain and Northern Ireland ({row.name})'}

    # Apply check to data
    try:
        # Load LOCA group to GeoPandas (assuming UK grid for now)
        location = tables['LOCA'].set_index('LOCA_ID')
        location['geometry'] = list(zip(location['LOCA_NATE'], location['LOCA_NATN']))
        location['geometry'] = location['geometry'].apply(Point)
        location = gpd.GeoDataFrame(location, geometry='geometry', crs='EPSG:27700')

        # Find locations outside gb or northern ireland
        result = location.apply(check_coordinates, axis=1)
        errors = result[result.notnull()].to_list()

    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


def check_locx_is_not_duplicate_of_other_column(tables: dict) -> List[dict]:
    """LOCA_LOCX and LOCA_LOCY are not duplicates of other columns"""

    def check_for_duplicates(row):
        """Return errors for rows that contain duplicates."""
        error = None

        if row['LOCA_NATE'] == row['LOCA_LOCX'] or row['LOCA_NATN'] == row['LOCA_LOCY']:
            error = {'line': '-', 'group': 'LOCA',
                     'desc': f'LOCX / LOCY duplicates NATE / NATN ({row.name})'}
        elif (float(row['LOCA_LON']) == row['LOCA_LOCX'] or
              float(row['LOCA_LAT']) == row['LOCA_LOCY']):
            error = {'line': '-', 'group': 'LOCA',
                     'desc': f'LOCX / LOCY duplicates LON / LAT ({row.name})'}

        return error

    # Apply check to data
    try:
        location = tables['LOCA'].set_index('LOCA_ID')
        result = location.apply(check_for_duplicates, axis=1)
        errors = result[result.notnull()].to_list()
    except KeyError:
        # LOCA not present, already checked in earlier rule
        pass

    return errors


BGS_RULES = {
    'Required Groups': check_required_groups,
    'Required BGS Groups': check_required_bgs_groups,
    'Spatial Referencing': check_spatial_referencing_system,
    'Eastings/Northings Present': check_eastings_northings_present,
    'Eastings/Northings Range': check_eastings_northings_range,
    'Drill Depth Present': check_drill_depth_present,
    'Drill Depth GEOL Record': check_drill_depth_geol_record,
    'LOCA within Great Britain': check_loca_within_great_britain,
    'LOCA_LOCX is not duplicate of other column': check_locx_is_not_duplicate_of_other_column,
}
