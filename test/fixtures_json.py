import datetime as dt

JSON_RESPONSES = {
    'example_ags.ags': {
        'filename': 'example_ags.ags',
        'filesize': 4105,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'All checks passed!',
        'errors': {},
        'valid': True,
        'additional_metadata': {}
    },
    'nonsense.AGS': {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'AGS Format Rule 2a': [{'line': 1,
                                    'group': '',
                                    'desc': 'Is not terminated by <CR> and <LF> characters.'}],
            'AGS Format Rule 3': [{'line': 1,
                                   'group': '',
                                   'desc': 'Does not start with a valid data descriptor.'}],
            'AGS Format Rule 5': [{'line': 1,
                                   'group': '',
                                   'desc': 'Contains fields that are not enclosed in double quotes.'}],
            'AGS Format Rule 13': [{'line': '-', 'group': 'PROJ', 'desc': 'PROJ group not found.'}],
            'AGS Format Rule 14': [{'line': '-', 'group': 'TRAN', 'desc': 'TRAN group not found.'}],
            'AGS Format Rule 15': [{'line': '-', 'group': 'UNIT', 'desc': 'UNIT group not found.'}],
            'AGS Format Rule 17': [{'line': '-', 'group': 'TYPE', 'desc': 'TYPE group not found.'}]},
        'valid': False,
        'additional_metadata': {}
    },
    'random_binary.ags': {
        'filename': 'random_binary.ags',
        'filesize': 1024,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '36 error(s) found in file!',
        'errors': {'AGS Format Rule 1': [{'desc': 'Has Non-ASCII character(s) and/or '
                                          'a byte-order-mark (BOM).',
                                          'group': '',
                                          'line': 1},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 2},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 3},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 4},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 5},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 6},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 7},
                                         {'desc': 'Has Non-ASCII character(s).',
                                          'group': '',
                                          'line': 8}],
                    'AGS Format Rule 13': [{'desc': 'PROJ group not found.',
                                            'group': 'PROJ',
                                            'line': '-'}],
                    'AGS Format Rule 14': [{'desc': 'TRAN group not found.',
                                            'group': 'TRAN',
                                            'line': '-'}],
                    'AGS Format Rule 15': [{'desc': 'UNIT group not found.',
                                            'group': 'UNIT',
                                            'line': '-'}],
                    'AGS Format Rule 17': [{'desc': 'TYPE group not found.',
                                            'group': 'TYPE',
                                            'line': '-'}],
                    'AGS Format Rule 2a': [{'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 1},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 2},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 3},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 4},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 5},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 6},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 7},
                                           {'desc': 'Is not terminated by <CR> and '
                                                    '<LF> characters.',
                                            'group': '',
                                            'line': 8}],
                    'AGS Format Rule 3': [{'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 1},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 2},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 3},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 4},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 5},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 6},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 7},
                                          {'desc': 'Does not start with a valid data '
                                                   'descriptor.',
                                           'group': '',
                                           'line': 8}],
                    'AGS Format Rule 5': [{'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 1},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 2},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 3},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 4},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 5},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 6},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 7},
                                          {'desc': 'Contains fields that are not '
                                                   'enclosed in double quotes.',
                                           'group': '',
                                           'line': 8}]},
        'valid': False,
        'additional_metadata': {}
    },
    'real/CG014058_F.ags': {
        'filename': 'CG014058_F.ags',
        'filesize': 50574,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '1 error(s) found in file!',
        'errors': {'AGS Format Rule 3': [{'desc': 'Line starts with "**PROJ" instead '
                                          'of a valid data descriptor. This '
                                          'indicates that file is in the AGS3 '
                                          'format which is not supported.',
                                          'group': '',
                                          'line': 1}]},
        'valid': False,
        'additional_metadata': {}
    },
    'real/Blackburn Southern Bypass.ags': {
        'filename': 'Blackburn Southern Bypass.ags',
        'filesize': 6566,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '95 error(s) found in file!',
        'errors': {'AGS Format Rule 1': [{'desc': 'Has Non-ASCII character(s) and/or '
                                          'a byte-order-mark (BOM).',
                                          'group': '',
                                          'line': 1}],
                   'AGS Format Rule 2a': [{'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 1},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 2},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 3},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 4},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 5},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 6},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 7},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 8},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 9},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 10},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 11},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 12},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 13},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 14},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 15},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 16},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 17},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 18},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 19},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 20},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 21},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 22},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 23},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 24},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 25},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 26},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 27},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 28},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 29},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 30},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 31},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 32},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 33},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 34},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 35},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 36},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 37},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 38},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 39},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 40},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 41},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 42},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 43},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 44},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 45},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 46},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 47},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 48},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 49},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 50},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 51},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 52},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 53},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 54},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 55},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 56},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 57},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 58},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 59},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 60},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 61},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 62},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 63},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 64},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 65},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 66},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 67},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 68},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 69},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 70},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 71},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 72},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 73},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 74},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 75},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 76},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 77},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 78},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 79},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 80},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 81},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 82},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 83},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 84},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 85},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 86},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 87},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 88},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 89},
                                          {'desc': 'Is not terminated by <CR> and '
                                           '<LF> characters.',
                                           'group': '',
                                           'line': 90}],
                   'AGS Format Rule 3': [{'desc': 'Does not start with a valid data '
                                          'descriptor.',
                                          'group': '',
                                          'line': 1}],
                   'AGS Format Rule 5': [{'desc': 'Contains fields that are not '
                                          'enclosed in double quotes.',
                                          'group': '',
                                          'line': 1}],
                   'AGS Format Rule 7': [{'desc': 'Headings not in order starting '
                                          'from LOCA_CHKG. Expected order: '
                                          '...LOCA_ORID|LOCA_ORJO|LOCA_ORCO|LOCA_CHKG|LOCA_APPG|LOCA_PDEP',
                                          'group': 'LOCA',
                                          'line': 86}],
                   'General': [{'desc': 'This file seems to be encoded with a '
                                'byte-order-mark (BOM). It is highly '
                                'recommended that the file be saved without '
                                'BOM encoding to avoid issues with other '
                                'sofware.',
                                'group': '',
                                'line': ''}]},
        'valid': False,
        'additional_metadata': {}
    },
    'real/A3040_03.ags': {
        'filename': 'A3040_03.ags',
        'filesize': 264526,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '1 error(s) found in file!',
        'errors': {'AGS Format Rule 3': [{'desc': 'Line starts with "**PROJ" instead '
                                          'of a valid data descriptor. This '
                                          'indicates that file is in the AGS3 '
                                          'format which is not supported.',
                                          'group': '',
                                          'line': 1}]},

        'valid': False,
        'additional_metadata': {}
    },
    'extension_is.bad': {
        'filename': 'extension_is.bad',
        'filesize': 0,
        'checkers': [],
        'dictionary': '',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '1 error(s) found in file!',
        'errors': {'File read error': [
            {'line': '-', 'group': '', 'desc': 'extension_is.bad is not an .ags file'}]},
        'valid': False,
        'additional_metadata': {}
    },
}

# These response values break the schema
BROKEN_JSON_RESPONSES = [
    {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'AGS Format Rule 2a': [{'line': '*',
                                    'group': '',
                                    'desc': ''}],
        },
        'valid': False,
        'additional_metadata': {}
    },
    {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'AGS Format Rule 0': [{'line': 1,
                                   'group': '',
                                   'desc': ''}],
        },
        'valid': False,
        'additional_metadata': {}
    },
]
