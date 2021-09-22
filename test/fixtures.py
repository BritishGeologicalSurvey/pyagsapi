"""Shared pytest data."""

FROZEN_TIME = "2021-08-23 14:25:43"

GOOD_FILE_DATA = [
    ('example_ags.ags', ('SUCCESS: example_ags.ags converted to example_ags.xlsx', 'example_ags.xlsx')),
    ('example_xlsx.xlsx', ('SUCCESS: example_xlsx.xlsx converted to example_xlsx.ags', 'example_xlsx.ags')),
]

BAD_FILE_DATA = [
    ('nonsense.ags', ('ERROR: File does not have AGS4 format layout', 9)),
    ('empty.ags', ('ERROR: File does not have AGS4 format layout', 0)),
    ('dummy.xlsx', ("ERROR: Bad spreadsheet layout ('DataFrame' object has no attribute 'HEADING')", 4787)),
    ('random_binary.ags', ('ERROR: File does not have AGS4 format layout', 1024)),
    ('real/A3040_03.ags', ("ERROR: File contains duplicate headers", 264526)),
    ('extension_is.bad', ("ERROR: extension_is.bad is not .ags or .xlsx format", 0)),
    ('real/JohnStPrimarySchool.ags', ("ERROR: UNIT and/or TYPE rows missing OR mismatched column numbers", 12430)),
    ('real/19684.ags', ("ERROR: File does not have AGS4 format layout", 12542)),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', ("ERROR: File contains duplicate headers", 0))
]

DICTIONARIES = {
    'v4_0_3': "Standard_dictionary_v4_0_3.ags",
    'v4_0_4': "Standard_dictionary_v4_0_4.ags",
    'v4_1': "Standard_dictionary_v4_1.ags"
}

BGS_RULES_ERRORS = {
    'sample_referencing_samp_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': "No parent id: SAMP_ID not in SAMP group (['A67890'])"},
        {'line': '-', 'group': 'SAMP',
         'desc': ("Inconsistent id: SAMP_ID A12345 has multiple component ids "
                  "(['327-16B,24.55,U,24', '327-16C,24.55,U,24'])")},
        {'line': '-', 'group': 'SAMP',
         'desc': ("Inconsistent id: SAMP_ID A98765 has multiple component ids "
                  "(['327-16E,24.55,B,24', '327-16E,24.55,U,24'])")},
    ],
    'sample_referencing_comp_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "No sample id: either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': ("No parent id: LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF not in SAMP group "
                  "(['CBH03,9.9,U,36', 'CBH03,nan,,'])")},
    ],
    'sample_referencing_mix_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "No sample id: either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': ("No parent id: LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF not in SAMP group "
                  "(['327-16C,24.55,U,24', '327-16D,24.55,U,24'])")},
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': "No parent id: SAMP_ID not in SAMP group (['A67890'])"},
    ]
}
