"""Shared pytest data."""
import os
from pathlib import Path

from app.version import API_VERSION as APP_VERSION

API_VERSION = f"/v{APP_VERSION.split('.')[0]}"

TEST_FILE_DIR = Path(__file__).parent / 'files'

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

FROZEN_TIME = "2021-08-23 14:25:43"

GOOD_FILE_DATA = [
    ('example_ags.ags', ('SUCCESS: example_ags.ags converted to example_ags.xlsx', 'example_ags.xlsx')),
    ('example_xlsx.xlsx', ('SUCCESS: example_xlsx.xlsx converted to example_xlsx.ags', 'example_xlsx.ags')),
]

BAD_FILE_DATA = [
    ('nonsense.AGS', ('No valid AGS4 data found in input file.', 9)),
    ('empty.ags', ('No valid AGS4 data found in input file.', 0)),
    ('dummy.xlsx', ("ERROR: Conversion failed", 4787)),
    ('random_binary.ags', ('No valid AGS4 data found in input file.', 1024)),
    ('real/AGS3/A3040_03.ags', ("ERROR: File contains duplicate headers", 264526)),
    ('extension_is.bad', ("ERROR: extension_is.bad is not .ags or .xlsx format", 0)),
    ('real/JohnStPrimarySchool.ags', ("Line 27 does not have the same number of entries "
                                      "as the HEADING row in GEOL.", 12430)),
    ('real/AGS3/19684.ags', ("No valid AGS4 data found in input file.", 12542))
]

ZIP_FILES_VALIDATE = {
    'one_good_ags.zip': ['example_ags.ags'],
    'two_good_ags.zip': ['example_ags.ags', 'example_fyis_ags.ags'],
    'one_good_two_bad_ags.zip': ['example_fyis_ags.ags', 'example_broken_ags.ags', 'nonsense.AGS'],
}

ZIP_FILES_CONVERT = {
    'one_good_ags.zip': ['example_ags.xlsx'],
    'two_good_ags.zip': ['example_ags.xlsx', 'example_fyis_ags.xlsx'],
    'one_good_two_bad_ags.zip': ['example_fyis_ags.xlsx'],
    'one_good_xlsx.zip': ['example_xlsx.ags'],
    'one_good_ags_one_good_xlsx.zip': ['example_xlsx.ags', 'example_fyis_ags.xlsx'],
}

DICTIONARIES = {
    'v4_0_3': "Standard_dictionary_v4_0_3.ags",
    'v4_0_4': "Standard_dictionary_v4_0_4.ags",
    'v4_1': "Standard_dictionary_v4_1.ags",
    'v4_1_1': "Standard_dictionary_v4_1_1.ags"
}

BGS_RULES_ERRORS = {
    'sample_referencing_samp_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id A12345: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Inconsistent id A99999: references duplicate component data"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Inconsistent id A11111: references duplicate component data"},
        {'line': '-', 'group': 'CONG',
         'desc': "No parent id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) not in SAMP group (['A67890'])"},
    ],
    'sample_referencing_comp_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "Record 1 is missing either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Record 4 is missing either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id CBH01,6.8,B,10: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': "Record 3 is missing either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'CONG',
         'desc': ("No parent id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) not in SAMP group "
                  "(['CBH03,9.9,U,36'])")},
    ],
    'sample_referencing_mix_ids.ags': [
        {'line': '-', 'group': 'SAMP',
         'desc': "Record 3 is missing either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
        {'line': '-', 'group': 'SAMP',
         'desc': ("Duplicate sample id 327-16A,24.55,U,24: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) "
                  "must be unique")},
        {'line': '-', 'group': 'SAMP',
         'desc': "Duplicate sample id A12345: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) must be unique"},
        {'line': '-', 'group': 'CONG',
         'desc': "Inconsistent id A67890: references duplicate component data"},
        {'line': '-', 'group': 'CONG',
         'desc': ("No parent id: SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF) not in SAMP group "
                  "(['327-16D,24.55,U,24', 'A67890'])")},
    ],
    'trit_group_test.ags': []  # There should be no duplicates reported
}
