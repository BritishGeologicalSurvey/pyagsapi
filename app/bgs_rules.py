"""Functions for each of the BGS data validation rules"""
from pathlib import Path
from typing import List

from shapely.geometry import Point
import geopandas as gpd
import pandas as pd

from app.bgs_group_id_keys import get_group_id_keys

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
UK_EEA_OUTLINE = Path(__file__).parent / 'uk_eea_area_ex_ni.geojson'
bgs_rules_version = '3.0.0'


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
    gb_outline = gpd.read_file(GB_OUTLINE).loc[0, 'geometry']
    ni_outline = gpd.read_file(NI_OUTLINE).loc[0, 'geometry']
    uk_eea_outline_wgs84 = gpd.read_file(UK_EEA_OUTLINE)
    uk_eea_outline = uk_eea_outline_wgs84.to_crs('EPSG:27700').loc[0, 'geometry']
    errors = []

    # Read data into geodataframe
    try:
        location = tables['LOCA'].set_index('LOCA_ID')
        location['geometry'] = list(zip(location['LOCA_NATE'], location['LOCA_NATN']))
    except KeyError:
        # LOCA not present, already checked in earlier rule
        return errors

    location['geometry'] = location['geometry'].apply(Point)
    location = gpd.GeoDataFrame(location, geometry='geometry', crs='EPSG:27700')
    location['line_no'] = range(1, len(location) + 1)

    inside_uk_eea_mask = location.intersects(uk_eea_outline)
    inside_gb_mask = location.intersects(gb_outline)
    as_irish_grid = location.to_crs("EPSG:29903")
    inside_ni_mask = as_irish_grid.intersects(ni_outline)
    outside_uk_eea_and_ni_mask = ~inside_uk_eea_mask & ~inside_ni_mask
    outside_gb_and_ni_mask = ~inside_gb_mask & ~inside_ni_mask

    for loca_id, row in location.loc[outside_uk_eea_and_ni_mask].iterrows():
        errors.append({
            'line': f'{row["line_no"]}', 'group': 'LOCA',
            'desc': f'NATE / NATN outside UK Offshore EEA or Onshore Northern Ireland boundary ({loca_id})'
        })

    for loca_id, row in location.loc[outside_gb_and_ni_mask].iterrows():
        errors.append({
            'line': f'{row["line_no"]}', 'group': 'LOCA',
            'desc': f'NATE / NATN outside Onshore Great Britain or Northern Ireland boundaries ({loca_id})'
        })

    for loca_id, row in location.loc[inside_ni_mask].iterrows():
        if row['LOCA_GREF']:
            continue
        else:
            errors.append({
                'line': f'{row["line_no"]}', 'group': 'LOCA',
                'desc': f'NATE / NATN in Northern Ireland but LOCA_GREF undefined ({loca_id})'
            })

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


def check_sample_referencing(tables: dict) -> List[dict]:
    """
       If a SAMP group exists it must:
        - have an identifier SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)
        - all identifiers must be unique

       For all child groups see bgs_group_id_keys:
        - have an identifier matching 'samp_id' or 'comp_id' for that group
        - all identifiers must be unique
        - the identifier SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)
          must appear in the SAMP group
    """

    def values_all_valid(row, id_keys):
        """ Return true if all the values are not null and not empty """
        for id_key in id_keys:
            if row[id_key] is None or row[id_key] == '':
                return False
        return True

    def id_from_keys(row, id_keys):
        """ Concatenate values to create id """
        values = [str(row[id_key]) for id_key in id_keys]
        id_ = ','.join(values)
        return id_

    def clean_ids(id_pairs: pd.DataFrame):
        #  Remove null pairs and fill blank sample ids with composite ids
        rows_without_any_nulls = id_pairs.notna().any(axis=1)
        id_pairs = id_pairs.loc[rows_without_any_nulls].copy()
        id_pairs['samp_id'].fillna(id_pairs['comp_id'], inplace=True)
        return id_pairs

    def id_pair(row, group):
        id_keys = get_group_id_keys(group)

        samp_id = None
        if (set(id_keys['samp_id_keys']) <= set(row.keys())
                and values_all_valid(row, id_keys['samp_id_keys'])):
            samp_id = id_from_keys(row, id_keys['samp_id_keys'])

        comp_id = None
        if (set(id_keys['comp_id_keys']) <= set(row.keys())
                and values_all_valid(row, id_keys['comp_id_keys'])):
            comp_id = id_from_keys(row, id_keys['comp_id_keys'])
        return pd.Series([samp_id, comp_id])

    def child_consistency(samp_ids, tables: dict) -> List[dict]:
        errors = []
        children = []
        for group in tables.keys():
            id_keys = get_group_id_keys(group)
            if ((set(id_keys['samp_id_keys']) <= set(tables[group].columns)
                    or set(id_keys['comp_id_keys']) <= set(tables[group].columns))
                    and group != 'SAMP'):
                children.append(group)

        for group in children:
            child_id_pairs = tables[group].apply(id_pair, axis=1, args=(group,))
            child_id_pairs.columns = ['samp_id', 'comp_id']
            errors, child_id_pairs = internal_consistency(group, child_id_pairs)

            # Parent ids refer to keys used by SAMP with extra fields
            parent_id_pairs = tables[group].apply(id_pair, axis=1, args=('SAMP',))
            parent_id_pairs.columns = ['samp_id', 'comp_id']
            parent_id_pairs = clean_ids(parent_id_pairs)

            if no_parent_ids := sorted(list(set(parent_id_pairs['samp_id']).difference(set(samp_ids)))):
                errors.append(
                    {'line': '-', 'group': f'{group}',
                     'desc': (f"No parent id: {','.join(id_keys['samp_id_keys'])} or "
                              f"({','.join(id_keys['comp_id_keys'])}) "
                              f"not in SAMP group ({no_parent_ids})")})
        return errors

    def internal_consistency(group: str, id_pairs: pd.DataFrame):
        errors = []
        id_keys = get_group_id_keys(group)

        # Check for missing IDs
        for row_id in id_pairs[id_pairs.isna().all(axis=1)].index.to_list():
            errors.append(
                {'line': '-', 'group': f'{group}',
                 'desc': f"Record {row_id + 1} is missing either "
                         f"{','.join(id_keys['samp_id_keys'])} or "
                         f"({','.join(id_keys['comp_id_keys'])})"})

        id_pairs = clean_ids(id_pairs)

        # Check for duplicate IDs
        for samp_id in sorted(list(set(id_pairs[id_pairs['samp_id'].duplicated()]['samp_id']))):
            errors.append(
                {'line': '-', 'group': f'{group}',
                 'desc': (f"Duplicate sample id {samp_id}: {','.join(id_keys['samp_id_keys'])} "
                          f"or ({','.join(id_keys['comp_id_keys'])}) "
                          f"must be unique")})
        # remove duplicate ids
        id_pairs = id_pairs[~ id_pairs['samp_id'].duplicated()]

        # Check for inconsistent IDs
        for samp_id in id_pairs[id_pairs['comp_id'].duplicated()]['samp_id']:
            errors.append(
                {'line': '-', 'group': f'{group}',
                 'desc': f'Inconsistent id {samp_id}: references duplicate component data'})

        return errors, id_pairs

    # Check data
    try:
        sample = tables['SAMP']
        samp_id_pairs = sample.apply(id_pair, axis=1, args=('SAMP',))
        samp_id_pairs.columns = ['samp_id', 'comp_id']
        errors, samp_id_pairs = internal_consistency('SAMP', samp_id_pairs)
        child_errors = child_consistency(samp_id_pairs['samp_id'], tables)
        errors.extend(child_errors)
    except KeyError:
        # group not in group list
        errors = []

    return errors


BGS_RULES = {
    'BGS data validation: Required Groups': check_required_groups,
    'BGS data validation: Required BGS Groups': check_required_bgs_groups,
    'BGS data validation: Spatial Referencing': check_spatial_referencing_system,
    'BGS data validation: Eastings/Northings Present': check_eastings_northings_present,
    'BGS data validation: Eastings/Northings Range': check_eastings_northings_range,
    'BGS data validation: Drill Depth Present': check_drill_depth_present,
    'BGS data validation: Drill Depth GEOL Record': check_drill_depth_geol_record,
    'BGS data validation: LOCA within Great Britain': check_loca_within_great_britain,
    'BGS data validation: LOCA_LOCX is not duplicate of other column': check_locx_is_not_duplicate_of_other_column,
    'BGS data validation: LOCA_ID references': check_loca_id_references_are_valid,
    'BGS data validation: Sample Referencing': check_sample_referencing,
}
