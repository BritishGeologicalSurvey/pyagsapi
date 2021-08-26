"""Functions for each of the BGS data validation rules"""


def check_required_groups(tables: dict) -> list:
    """ Groups must include PROJ, LOCA or HOLE, ABBR, TYPE, UNIT """
    errors = []
    desc = ''
    required = ['PROJ', 'ABBR', 'TYPE', 'UNIT']
    for group in required:
        if group not in tables.keys():
            desc += group + ', '
    if 'LOCA' not in tables.keys() and 'HOLE' not in tables.keys():
        desc += '(LOCA or HOLE)' + ', '
    if desc:
        desc = 'Required groups not present: ' + desc
        desc = desc.rstrip(', ')
    if desc:
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


def check_required_bgs_groups(tables: dict) -> list:
    """ Groups must include GEOL for BGS """
    errors = []
    desc = ''
    group = 'GEOL'
    if group not in tables.keys():
        desc += f'Required BGS groups not present: {group}'
    if desc:
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


BGS_RULES = {
    'Required Groups': check_required_groups,
    'Required BGS Groups': check_required_bgs_groups,
}
