"""Shared pytest data."""

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

VALIDATION_TEXT_RSP_DATA = [
    ('example1.ags', ('All checks passed!', 3)),
    ('nonsense.ags', (r'7 error\(s\) found in file!', 0)),
    ('empty.ags', (r'4 error\(s\) found in file!', 0)),
    ('real/A3040_03.ags', (r'5733 error\(s\) found in file!', 258)),
    ('example1.xlsx', ('ERROR: Only .ags files are accepted as input.', 11)),
    ('random_binary.ags', ('ERROR: Unreadable character "á" at position 1 on line: 1\nStarting:', 1)),
    ('real/CG014058_F.ags', (r'ERROR: Unreadable character "æ" at position 80 on line: 263\nStarting: "WS2"', 49)),
    ('real/Blackburn Southern Bypass.ags', (r'93 error\(s\) found in file!', 6)),  # this file contains BOM character
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
