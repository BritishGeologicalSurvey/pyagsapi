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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
    'example_broken_ags.ags': {
        "filename": "example_broken_ags.ags",
        "filesize": 4111,
        "checkers": ["python_ags4 v0.5.0"],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        "message": "13 error(s) found in file!",
        "errors": {
            "AGS Format Rule 4": [
                {
                    "line": 31,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                },
                {
                    "line": 34,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                },
                {
                    "line": 36,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                }
            ],
            "AGS Format Rule 5": [
                {
                    "line": 31,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 32,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 34,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 35,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 36,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 37,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                }
            ],
            "AGS Format Rule 3": [
                {
                    "line": 32,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                },
                {
                    "line": 35,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                },
                {
                    "line": 37,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                }
            ],
            "AGS Format Rule ?": [
                {
                    "line": "-",
                    "group": "",
                    "desc": "Line 31 does not have the same number of entries as the HEADING row in TYPE."
                }
            ],
        },
        "valid": False,
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
    'random_binary.ags': {
        'filename': 'random_binary.ags',
        'filesize': 1024,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '37 error(s) found in file!',
        'errors': {'AGS Format Rule 1': [{'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8') "
                                          "and/or a byte-order-mark (BOM).",
                                          'group': '',
                                          'line': 1},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 2},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 3},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 4},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 5},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 6},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
                                          'group': '',
                                          'line': 7},
                                         {'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8').",
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
                                           'line': 8}],
                   'General': [{'line': '',
                                'group': '',
                                'desc': "AGS4 Rule 1 is interpreted as allowing both standard ASCII characters "
                                "(Unicode code points 0-127) and extended ASCII characters (Unicode code points "
                                "160-255). Please beware that extended ASCII characters differ based on the "
                                "encoding used when the file was created. The validator defaults to 'utf-8' "
                                "encoding as it is the most widely used encoding compatible with Unicode. The user "
                                "can override this default if the file encoding is different but, it is highly "
                                "recommended that the 'utf-8' encoding be used when creating AGS4 files. (Hint: "
                                "If not 'utf-8', then the encoding is most likely to be 'windows-1252' "
                                "aka 'cp1252')"}]},
        'valid': False,
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
    'real/AGS3/CG014058_F.ags': {
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
    'real/Blackburn Southern Bypass.ags': {
        'filename': 'Blackburn Southern Bypass.ags',
        'filesize': 6566,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '95 error(s) found in file!',
        'errors': {'AGS Format Rule 1': [{'desc': "Has Non-ASCII character(s) "
                                          "(assuming that file encoding is 'utf-8') "
                                          "and/or a byte-order-mark (BOM).",
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
                   'General': [{'line': '',
                                'group': '',
                                'desc': "AGS4 Rule 1 is interpreted as allowing both standard ASCII characters "
                                "(Unicode code points 0-127) and extended ASCII characters (Unicode code points "
                                "160-255). Please beware that extended ASCII characters differ based on the "
                                "encoding used when the file was created. The validator defaults to 'utf-8' "
                                "encoding as it is the most widely used encoding compatible with Unicode. The user "
                                "can override this default if the file encoding is different but, it is highly "
                                "recommended that the 'utf-8' encoding be used when creating AGS4 files. (Hint: "
                                "If not 'utf-8', then the encoding is most likely to be 'windows-1252' aka 'cp1252')"},
                               {'line': '',
                                'group': '',
                                'desc': 'This file seems to be encoded with a byte-order-mark (BOM). '
                                'It is highly recommended that the file be saved without BOM encoding '
                                'to avoid issues with other software.'}]},
        'valid': False,
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
    'real/AGS3/A3040_03.ags': {
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
}

GEOJSON_RESPONSES = {
    'example_ags.ags': {
        'filename': 'example_ags.ags',
        'filesize': 4105,
        'checkers': ['python_ags4 v0.5.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'All checks passed!',
        'errors': {},
        'valid': True,
        'additional_metadata': {},
        'geojson': {
            'features': [{
                'geometry': {
                    'coordinates': [-0.22760675836552394, 51.491649521233036],
                    'type': 'Point'},
                'id': '121415.327-16A',
                'properties': {
                    'LOCA_ALID': '',
                    'LOCA_CLST': '',
                    'LOCA_CNGE': '',
                    'LOCA_DATM': '',
                    'LOCA_ELAT': '',
                    'LOCA_ELON': '',
                    'LOCA_ENDD': '',
                    'LOCA_ETRV': None,
                    'LOCA_FDEP': None,
                    'LOCA_FILE_FSET': '',
                    'LOCA_GL': None,
                    'LOCA_GREF': '',
                    'LOCA_ID': '327-16A',
                    'LOCA_LAT': '',
                    'LOCA_LETT': '',
                    'LOCA_LLZ': '',
                    'LOCA_LOCA': '',
                    'LOCA_LOCM': '',
                    'LOCA_LOCX': None,
                    'LOCA_LOCY': None,
                    'LOCA_LOCZ': None,
                    'LOCA_LON': '',
                    'LOCA_LREF': '',
                    'LOCA_LTRV': None,
                    'LOCA_NATE': 523145.0,
                    'LOCA_NATN': 178456.12,
                    'LOCA_NTRV': None,
                    'LOCA_OFFS': None,
                    'LOCA_PURP': '',
                    'LOCA_REM': '',
                    'LOCA_STAR': '',
                    'LOCA_STAT': '',
                    'LOCA_TERM': '',
                    'LOCA_TRAN': '',
                    'LOCA_TYPE': '',
                    'LOCA_XTRL': None,
                    'LOCA_YTRL': None,
                    'LOCA_ZTRL': None,
                    'PROJ_CLNT': 'ACME Enterprises',
                    'PROJ_CONT': 'ACME Drilling Ltd',
                    'PROJ_ENG': '',
                    'PROJ_FILE_FSET': '',
                    'PROJ_ID': '121415',
                    'PROJ_LOC': 'Anytown',
                    'PROJ_MEMO': '',
                    'PROJ_NAME': 'ACME Gas Works Redevelopment',
                    'line_no': 1},
                'type': 'Feature'}],
            'type': 'FeatureCollection'},
        'geojson_error': None
    },
    'example_broken_ags.ags': {
        "filename": "example_broken_ags.ags",
        "filesize": 4111,
        "checkers": ["python_ags4 v0.5.0"],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        "message": "13 error(s) found in file!",
        "errors": {
            "AGS Format Rule 4": [
                {
                    "line": 31,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                },
                {
                    "line": 34,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                },
                {
                    "line": 36,
                    "group": "TYPE",
                    "desc": "Number of fields does not match the HEADING row."
                }
            ],
            "AGS Format Rule 5": [
                {
                    "line": 31,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 32,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 34,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 35,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 36,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                },
                {
                    "line": 37,
                    "group": "",
                    "desc": "Contains fields that are not enclosed in double quotes."
                }
            ],
            "AGS Format Rule 3": [
                {
                    "line": 32,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                },
                {
                    "line": 35,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                },
                {
                    "line": 37,
                    "group": "",
                    "desc": "Does not start with a valid data descriptor."
                }
            ],
            "AGS Format Rule ?": [
                {
                    "line": "-",
                    "group": "",
                    "desc": "Line 31 does not have the same number of entries as the HEADING row in TYPE."
                }
            ],
        },
        "valid": False,
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': 'Line 31 does not have the same number of entries as the HEADING row in TYPE.'
    }
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
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
        'additional_metadata': {},
        'geojson': {},
        'geojson_error': None
    },
]
