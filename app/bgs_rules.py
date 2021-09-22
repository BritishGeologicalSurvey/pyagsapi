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
        errors = []

    return errors


def check_locx_is_not_duplicate_of_other_column(tables: dict) -> List[dict]:
    """LOCA_LOCX and LOCA_LOCY are not duplicates of other columns"""

    def check_for_duplicates(row):
        """Return errors for rows that contain duplicates."""
        error = None

        if row['LOCA_NATE'] == row['LOCA_LOCX'] or row['LOCA_NATN'] == row['LOCA_LOCY']:
            error = {'line': '-', 'group': 'LOCA',
                     'desc': f'LOCX / LOCY duplicates NATE / NATN ({row.name})'}
        elif row['LOCA_LON'] == '' and row['LOCA_LAT'] == '':
            error = None
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
        errors = []


def unique_ids(samp_ids: List[str]) -> List[dict]:
    errors = []
    if len(samp_ids) > len(set(samp_ids)):
        errors.append(
            {'line': '-', 'group': 'SAMP',
             'desc': 'Duplicate sample id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique'})
    return errors


def orphans_samp(samp_ids: List[str], tables: dict) -> List[dict]:
    errors = []
    children = {group: table for group, table in tables.items() if 'SAMP_ID' in table.columns}
    for group, child in children.items():
        if group == 'SAMP':
            continue
        child_ids = set(child[child['SAMP_ID'] != '']['SAMP_ID'])
        if no_parent_ids := sorted(list(child_ids.difference(set(samp_ids)))):
            errors.append(
                {'line': '-', 'group': f'{group}',
                 'desc': f'No parent id: SAMP_ID not in SAMP group ({no_parent_ids})'})
    return errors


def orphans_comp(samp_ids: List[str], tables: dict) -> List[dict]:
    errors = []
    children = {group: table for group, table in tables.items()
                if {'LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF'} <= set(table.columns)}
    for group, child in children.items():
        if group == 'SAMP':
            continue
        child_ids = set(composite_ids(child))
        if no_parent_ids := sorted(list(child_ids.difference(set(samp_ids)))):
            errors.append(
                {'line': '-', 'group': f'{group}',
                 'desc': f'No parent id: LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF not in SAMP group ({no_parent_ids})'})
    return errors


def composite_ids(df):
    return list((df['LOCA_ID'] + ',' +
                 df['SAMP_TOP'].astype(str) + ',' +
                 df['SAMP_TYPE'] + ',' +
                 df['SAMP_REF']))


def valid_comp_ids(df):
    valid_ids = df[(df['LOCA_ID'] != '') &
                   (df['SAMP_TOP'].notna()) &
                   (df['SAMP_TYPE'] != '') &
                   (df['SAMP_REF'] != '')]
    return composite_ids(valid_ids)


def check_sample_referencing(tables: dict) -> List[dict]:
    """If a SAMP group exists it must:
        - have an identifier SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)
        - all identifiers must be unique
        - for any children of SAMP, child IDs must appear in SAMP group
    """
    errors = []
    try:
        sample = tables['SAMP']
        if all(sample['SAMP_ID'] != ''):
            # All SAMP_ID have a value, check samp_ids only
            samp_ids = list(sample['SAMP_ID'])
            errors.extend(unique_ids(samp_ids))
            errors.extend(orphans_samp(samp_ids, tables))
        elif all(sample['SAMP_ID'] == ''):
            # No SAMP_ID have a value, check composite ids only
            samp_ids = valid_comp_ids(sample)
            if len(samp_ids) < len(sample):
                errors.append(
                    {'line': '-', 'group': 'SAMP',
                     'desc': 'No sample id: either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)'})
            errors.extend(unique_ids(samp_ids))
            errors.extend(orphans_comp(samp_ids, tables))
        else:
            # Some SAMP_ID have a value, check both types of id
            samp_ids = list(sample[sample['SAMP_ID'] != '']['SAMP_ID'])
            comp_ids = valid_comp_ids(sample[sample['SAMP_ID'] == ''])
            if len(samp_ids) + len(comp_ids) < len(sample):
                errors.append(
                    {'line': '-', 'group': 'SAMP',
                     'desc': 'No sample id: either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)'})
            errors.extend(unique_ids(comp_ids))
            errors.extend(orphans_comp(comp_ids, tables))
            errors.extend(unique_ids(samp_ids))
            errors.extend(orphans_samp(samp_ids, tables))

    except KeyError:
        # SAMP not present
        pass

    return errors


def check_loca_id_references_are_valid(tables: dict) -> List[dict]:
    """Groups that have LOCA_ID column have populated it with valid record"""
    errors = []
    # Extract IDs from LOCA table
    try:
        loca_ids = tables['LOCA']['LOCA_ID'].unique()
    except KeyError:
        # LOCA not present, already checked in earlier rule
        return errors

    tables_referencing_loca = [table_name for table_name in tables.keys()
                               if 'LOCA_ID' in tables[table_name].columns
                               and table_name != 'LOCA']

    # Check each table for valid references
    for table in tables_referencing_loca:
        # define check function here because value of `table` changes.
        def check_loca_references(row):
            # table, loca_ids are taken from enclosing scope
            if not row['LOCA_ID']:
                # Record number is 0-indexed in name column
                error = {'line': '-', 'group': table,
                         'desc': f'Record {row.name + 1} has missing LOCA_ID'}
            elif row['LOCA_ID'] not in loca_ids:
                error = {'line': '-', 'group': table,
                         'desc': f'LOCA_ID ({row["LOCA_ID"]}) is not found in LOCA group'}
            else:
                error = None

            return error

        # Run check and add result to error list
        result = tables[table].apply(check_loca_references, axis=1)
        errors.extend(result[result.notnull()].to_list())

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
<<<<<<< HEAD
    'LOCA_ID references': check_loca_id_references_are_valid,
=======
    'Sample Referencing': check_sample_referencing,
>>>>>>> Add basic function and failing test
}
