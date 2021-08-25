"""Shared pytest data."""

FROZEN_TIME = "2021-08-23 14:25:43"

ISVALID_RSP_DATA = [
    ('example1.ags', True),
    ('nonsense.ags', False),
    ('empty.ags', False),
    ('real/A3040_03.ags', False),
    ('example1.xlsx', False),
    ('random_binary.ags', False),
    ('real/CG014058_F.ags', False),
    ('real/Blackburn Southern Bypass.ags', False),  # this file contains BOM character
]

GOOD_FILE_DATA = [
    ('example1.ags', 'SUCCESS: example1.ags converted to example1.xlsx'),
    ('example1.xlsx', 'SUCCESS: example1.xlsx converted to example1.ags'),
]

BAD_FILE_DATA = [
    ('nonsense.ags', ('IndexError: At least one sheet must be visible', 0)),
    ('empty.ags', ('IndexError: At least one sheet must be visible', 0)),
    ('dummy.xlsx', ("AttributeError: 'DataFrame' object has no attribute 'HEADING'", 5)),
    ('random_binary.ags', ('IndexError: At least one sheet must be visible', 1)),
    ('real/A3040_03.ags', ("UnboundLocalError: local variable 'group' referenced before assignment", 258)),
]
