"""Shared pytest data."""

FROZEN_TIME = "2021-08-23 14:25:43"

ISVALID_RSP_DATA = [
    ('example_ags.ags', True),
    ('nonsense.ags', False),
    ('empty.ags', False),
    ('real/A3040_03.ags', False),
    ('example_xlsx.xlsx', False),
    ('random_binary.ags', False),
    ('real/CG014058_F.ags', False),
    ('real/Blackburn Southern Bypass.ags', False),  # this file contains BOM character
    ('extension_is.bad', False),
]

GOOD_FILE_DATA = [
    ('example_ags.ags', ('SUCCESS: example_ags.ags converted to example_ags.xlsx', 'example_ags.xlsx')),
    ('example_xlsx.xlsx', ('SUCCESS: example_xlsx.xlsx converted to example_xlsx.ags', 'example_xlsx.ags')),
]

BAD_FILE_DATA = [
    ('nonsense.ags', ('ERROR: File does not have AGS format layout', 9)),
    ('empty.ags', ('ERROR: File does not have AGS format layout', 0)),
    ('dummy.xlsx', ("ERROR: Bad spreadsheet layout ('DataFrame' object has no attribute 'HEADING')", 4787)),
    ('random_binary.ags', ('ERROR: File does not have AGS format layout', 1024)),
    ('real/A3040_03.ags', ("ERROR: File contains duplicate headers", 264526)),
    ('extension_is.bad', ("ERROR: extension_is.bad is not .ags or .xlsx format", 0)),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', ("ERROR: File contains duplicate headers", 0))
]

DICTIONARIES = {
    'v4_0_3': "Standard_dictionary_v4_0_3.ags",
    'v4_0_4': "Standard_dictionary_v4_0_4.ags",
    'v4_1': "Standard_dictionary_v4_1.ags"
}
