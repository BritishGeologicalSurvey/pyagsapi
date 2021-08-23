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
