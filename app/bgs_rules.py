"""Functions for each of the BGS data validation rules"""
from typing import List

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


BGS_RULES = {
    'Required Groups': check_required_groups,
    'Required BGS Groups': check_required_bgs_groups,
    'Spatial Referencing': check_spatial_referencing_system,
    'Eastings/Northings Present': check_eastings_northings_present,
    'Eastings/Northings Range': check_eastings_northings_range,
    'Drill Depth Present': check_drill_depth_present,
    'Drill Depth GEOL Record': check_drill_depth_geol_record,
}
