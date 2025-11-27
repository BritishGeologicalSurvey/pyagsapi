import datetime as dt

JSON_RESPONSES = {
    'example_ags.ags': {
        'filename': 'example_ags.ags',
        'filesize': 4105,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'No errors found!',
        'errors': {},
        'valid': True,
        'additional_metadata': {'bgs_all_groups': '7 groups identified in file: PROJ '
                                'ABBR TRAN TYPE UNIT LOCA SAMP',
                                'bgs_dict': 'Optional DICT group present: False',
                                'bgs_file': 'Optional FILE group present: False',
                                'bgs_loca_rows': '1 data row(s) in LOCA group',
                                'bgs_projects': None},
        'error_count': 0,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'example_fyis_ags.ags': {
        'filename': 'example_fyis_ags.ags',
        'filesize': 4075,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'No errors found! 3 FYI(s) found in file.',
        'errors': {
            'FYI (Related to Rule 1)': [
                {
                    'desc': 'Has extended ASCII character(s).',
                    'group': '',
                    'line': 21,
                },
            ],
            'FYI (Related to Rule 16)': [
                {
                    'desc': 'DICT_TYPE: Description of abbreviation "GROUP" is "Group" but it '
                    'should be "Flag to indicate definition is a GROUP" according to '
                    'the standard abbreviations list.',
                    'group': 'ABBR',
                    'line': 11,
                },
            ],
            'FYI': [
                {
                    'desc': "'1.1' in TRAN_AGS is not a recognized AGS4 version. Therefore, "
                    'v4.1.1 of the standard dictionary will be used for validation '
                    'unless a different version is specified in the validator input.',
                    'group': 'TRAN',
                    'line': 21,
                },
            ],
        },
        'valid': True,
        'additional_metadata': {'bgs_all_groups': '7 groups identified in file: PROJ '
                                'ABBR TRAN TYPE UNIT LOCA SAMP',
                                'bgs_dict': 'Optional DICT group present: False',
                                'bgs_file': 'Optional FILE group present: False',
                                'bgs_loca_rows': '1 data row(s) in LOCA group',
                                'bgs_projects': None},
        'error_count': 0,
        'warnings_count': 0,
        'fyi_count': 2,
        'geojson': {},
        'geojson_error': None
    },
    'example_broken_ags.ags': {
        "filename": "example_broken_ags.ags",
        "filesize": 4078,
        "checkers": ["python_ags4 v1.1.0"],
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
            'General': [
                {
                    'desc': 'Could not complete validation. Please fix listed errors and try again.',
                    'group': '',
                    'line': '-',
                },
            ],
            'Validator Process Error': [
                {
                    "line": "-",
                    "group": "",
                    "desc": "Line 31 does not have the same number of entries as the HEADING row in TYPE."
                }
            ],
        },
        "valid": False,
        'additional_metadata': {},
        'error_count': 13,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'nonsense.AGS': {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v1.1.0'],
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
        'additional_metadata': {'bgs_all_groups': '0 groups identified in file: ',
                                'bgs_dict': 'Optional DICT group present: False',
                                'bgs_file': 'Optional FILE group present: False',
                                'bgs_projects': None},
        'error_count': 7,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'random_binary.ags': {
        'filename': 'random_binary.ags',
        'filesize': 1024,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '36 error(s) found in file!',
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
        'additional_metadata': {'bgs_all_groups': '0 groups identified in file: ',
                                'bgs_dict': 'Optional DICT group present: False',
                                'bgs_file': 'Optional FILE group present: False',
                                'bgs_projects': None},
        'error_count': 36,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'real/AGS3/CG014058_F.ags': {
        'filename': 'CG014058_F.ags',
        'filesize': 50574,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '2 error(s) found in file!',
        'errors': {'AGS Format Rule 3': [{'desc': 'Line starts with "**PROJ" instead '
                                          'of a valid data descriptor. This '
                                          'indicates that file is in the AGS3 '
                                          'format which is not supported.',
                                          'group': '',
                                          'line': 1}],
                   'Validator Process Error': [{'desc': 'Validation terminated due to suspected '
                                                'AGS3 file. Please fix errors and try again.',
                                                'group': '',
                                                'line': '-'}]},
        'valid': False,
        'additional_metadata': {},
        'error_count': 2,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'real/Blackburn Southern Bypass.ags': {
        'filename': 'Blackburn Southern Bypass.ags',
        'filesize': 6566,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '93 error(s) found in file!',
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
        'error_count': 93,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'real/AGS3/A3040_03.ags': {
        'filename': 'A3040_03.ags',
        'filesize': 264526,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '2 error(s) found in file!',
        'errors': {'AGS Format Rule 3': [{'desc': 'Line starts with "**PROJ" instead '
                                          'of a valid data descriptor. This '
                                          'indicates that file is in the AGS3 '
                                          'format which is not supported.',
                                          'group': '',
                                          'line': 1}],
                   'Validator Process Error': [{'desc': 'Validation terminated due to suspected '
                                                'AGS3 file. Please fix errors and try again.',
                                                'group': '',
                                                'line': '-'}]},

        'valid': False,
        'additional_metadata': {},
        'error_count': 2,
        'warnings_count': 0,
        'fyi_count': 0,
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
        'error_count': 1,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    'real/Fenham Barracks - Newcastle upon Tyne.ags': {
        "filename": "Fenham Barracks - Newcastle upon Tyne.ags",
        "filesize": 8561,
        "checkers": [
            "python_ags4 v1.1.0"
        ],
        "dictionary": "Standard_dictionary_v4_1_1.ags",
        "time": dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        "message": "98 error(s) found in file! 5 FYI(s) found in file.",
        "errors": {
            "AGS Format Rule 2a": [
                {
                    "line": 1,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 2,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 3,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 4,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 5,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 6,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 7,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 8,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 9,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 10,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 11,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 12,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 13,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 14,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 15,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 16,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 17,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 18,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 19,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 20,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 21,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 22,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 23,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 24,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 25,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 26,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 27,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 28,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 29,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 30,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 31,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 32,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 33,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 34,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 35,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 36,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 37,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 38,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 39,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 40,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 41,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 42,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 43,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 44,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 45,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 46,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 47,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 48,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 49,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 50,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 51,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 52,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 53,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 54,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 55,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 56,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 57,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 58,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 59,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 60,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 61,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 62,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 63,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 64,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 65,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 66,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 67,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 68,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 69,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 70,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 71,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 72,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 73,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 74,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 75,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 76,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 77,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 78,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 79,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 80,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 81,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 82,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 83,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 84,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 85,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 86,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                },
                {
                    "line": 87,
                    "group": "",
                    "desc": "Is not terminated by <CR> and <LF> characters."
                }
            ],
            "AGS Format Rule 14": [
                {
                    "line": 45,
                    "group": "TRAN",
                    "desc": "There should not be more than one DATA row in the TRAN group."
                },
                {
                    "line": 46,
                    "group": "TRAN",
                    "desc": "There should not be more than one DATA row in the TRAN group."
                }
            ],
            "AGS Format Rule 7": [
                {
                    "line": 2,
                    "group": "PROJ",
                    "desc": "Order of headings could not be checked as one or more fields "
                    "were not found in either the DICT group or the standard dictionary. "
                    "Check error log under AGS Format Rule 9."
                },
                {
                    "line": 8,
                    "group": "LOCA",
                    "desc": "Headings not in order starting from LOCA_FDEP. Expected order: "
                    "...LOCA_ID|LOCA_NATE|LOCA_NATN|LOCA_GL|LOCA_REM|LOCA_FDEP"
                },
                {
                    "line": 17,
                    "group": "GEOL",
                    "desc": "Headings not in order starting from GEOL_BASE. Expected order: "
                    "...GEOL_TOP|GEOL_BASE|GEOL_DESC|GEOL_LEG|GEOL_GEO2"
                }
            ],
            "AGS Format Rule 9": [
                {
                    "line": 2,
                    "group": "PROJ",
                    "desc": "PROJ_AGS not found in DICT group or the standard AGS4 dictionary."
                }
            ],
            "AGS Format Rule 10a": [
                {
                    "line": 44,
                    "group": "TRAN",
                    "desc": "Duplicate key field combination: DATA|1"
                },
                {
                    "line": 45,
                    "group": "TRAN",
                    "desc": "Duplicate key field combination: DATA|1"
                },
                {
                    "line": 46,
                    "group": "TRAN",
                    "desc": "Duplicate key field combination: DATA|1"
                }
            ],
            "AGS Format Rule 10b": [
                {
                    "line": 58,
                    "group": "UNIT",
                    "desc": "Empty REQUIRED fields: DATA|??UNIT_UNIT??|??UNIT_DESC??"
                }
            ],
            "AGS Format Rule 18": [
                {
                    "line": "-",
                    "group": "DICT",
                    "desc": "DICT group not found. See error log under AGS Format Rule 9 for a "
                    "list of non-standard headings that need to be defined in a DICT group."
                }
            ],
            "FYI (Related to Rule 16)": [
                {
                    "line": 67,
                    "group": "ABBR",
                    "desc": "GEOL_LEG: Description of abbreviation \"102\" is \"102\" but it should be "
                    "\"MADE GROUND\" according to the standard abbreviations list."
                },
                {
                    "line": 68,
                    "group": "ABBR",
                    "desc": "GEOL_LEG: Description of abbreviation \"202\" is \"202\" but it should be "
                    "\"Silty CLAY\" according to the standard abbreviations list."
                },
                {
                    "line": 69,
                    "group": "ABBR",
                    "desc": "GEOL_LEG: Description of abbreviation \"203\" is \"203\" but it should be "
                    "\"Sandy CLAY\" according to the standard abbreviations list."
                },
                {
                    "line": 70,
                    "group": "ABBR",
                    "desc": "GEOL_LEG: Description of abbreviation \"207\" is \"207\" but it should be "
                    "\"Silty sandy CLAY\" according to the standard abbreviations list."
                },
                {
                    "line": 71,
                    "group": "ABBR",
                    "desc": "GEOL_LEG: Description of abbreviation \"803\" is \"803\" but it should be "
                    "\"SANDSTONE\" according to the standard abbreviations list."
                }
            ]
        },
        "valid": False,
        "additional_metadata": {
            "bgs_projects": None,
            "bgs_all_groups": "7 groups identified in file: PROJ LOCA GEOL TRAN TYPE UNIT ABBR",
            "bgs_loca_rows": "4 data row(s) in LOCA group",
            "bgs_dict": "Optional DICT group present: False",
            "bgs_file": "Optional FILE group present: False"
        },
        'error_count': 98,
        'warnings_count': 0,
        'fyi_count': 5,
        'geojson': {},
        'geojson_error': None
    }
}


GEOJSON_RESPONSES = {
    'example_ags.ags': {
        'filename': 'example_ags.ags',
        'filesize': 4105,
        'checkers': ['python_ags4 v1.1.0'],
        'dictionary': 'Standard_dictionary_v4_1_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'No errors found! 1 FYI(s) found in file.',
        'errors': {},
        'valid': True,
        'additional_metadata': {},
        'error_count': 0,
        'warnings_count': 0,
        'fyi_count': 1,
        'geojson': {
            'features': [{
                'geometry': {
                    'coordinates': [-0.227606758365524, 51.491649521233036],
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
        "checkers": ["python_ags4 v1.1.0"],
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
            'General': [
                {
                    'desc': 'Could not complete validation. Please fix listed errors and try again.',
                    'group': '',
                    'line': '-',
                },
            ],
            'Validator Process Error': [
                {
                    "line": "-",
                    "group": "",
                    "desc": "Line 31 does not have the same number of entries as the HEADING row in TYPE."
                }
            ],
        },
        "valid": False,
        'additional_metadata': {},
        'error_count': 13,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': 'Line 31 does not have the same number of entries as the HEADING row in TYPE.'
    }
}

# These response values break the schema
BROKEN_JSON_RESPONSES = [
    {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v1.1.0'],
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
        'error_count': 7,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
    {
        'filename': 'nonsense.AGS',
        'filesize': 9,
        'checkers': ['python_ags4 v1.1.0'],
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
        'error_count': 7,
        'warnings_count': 0,
        'fyi_count': 0,
        'geojson': {},
        'geojson_error': None
    },
]

UNKNOWN_RULES_RESPONSE = {
    'detail': [
        {
            'ctx': {'expected': "'ags' or 'bgs'"},
            'input': 'unknown',
            'loc': ['body', 'checkers', 1],
            'msg': "Input should be 'ags' or 'bgs'",
            'type': 'enum'
        }
    ]
}
