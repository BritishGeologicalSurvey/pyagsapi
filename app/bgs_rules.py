"""Functions for each of the BGS data validation rules"""
from python_ags4 import AGS4


def check_required_groups(tables: dict) -> list:
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


def check_required_bgs_groups(tables: dict) -> list:
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


def check_spatial_referencing_system(tables: dict) -> list:
    """ Spatial referencing system defined in LOCA_GREF, LOCA_LREF or LOCA_LLZ """
    errors = []
    try:
        ref_found = False
        loca = AGS4.convert_to_numeric(tables['LOCA'])
        for col in ['LOCA_GREF', 'LOCA_LREF', 'LOCA_LLZ']:
            try:
                if all(loca[col] != ''):
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


BGS_RULES = {
    'Required Groups': check_required_groups,
    'Required BGS Groups': check_required_bgs_groups,
    'Spatial Referencing': check_spatial_referencing_system,
}
