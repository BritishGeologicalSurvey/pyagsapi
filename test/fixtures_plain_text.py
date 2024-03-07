# flake8: noqa
PLAIN_TEXT_RESPONSES = {
    'example_ags.ags': """
================================================================================
example_ags.ags: All checks passed!

# Metadata

File size: 4105 bytes
Checkers: ['python_ags4 v0.5.0']
Dictionary: Standard_dictionary_v4_1_1.ags
Time: 2021-08-23 14:25:43+00:00


================================================================================
""",
    'example_broken_ags.ags': """
================================================================================
example_broken_ags.ags: 13 error(s) found in file!

# Metadata

File size: 4111 bytes
Checkers: ['python_ags4 v0.5.0']
Dictionary: Standard_dictionary_v4_1_1.ags
Time: 2021-08-23 14:25:43+00:00


# Errors

## AGS Format Rule 4

Line: 31 - Number of fields does not match the HEADING row.
Line: 34 - Number of fields does not match the HEADING row.
Line: 36 - Number of fields does not match the HEADING row.

## AGS Format Rule 5

Line: 31 - Contains fields that are not enclosed in double quotes.
Line: 32 - Contains fields that are not enclosed in double quotes.
Line: 34 - Contains fields that are not enclosed in double quotes.
Line: 35 - Contains fields that are not enclosed in double quotes.
Line: 36 - Contains fields that are not enclosed in double quotes.
Line: 37 - Contains fields that are not enclosed in double quotes.

## AGS Format Rule 3

Line: 32 - Does not start with a valid data descriptor.
Line: 35 - Does not start with a valid data descriptor.
Line: 37 - Does not start with a valid data descriptor.

## AGS Format Rule ?

Group:  - Line 31 does not have the same number of entries as the HEADING row in TYPE.

================================================================================
""",
    'nonsense.AGS': """
================================================================================
nonsense.AGS: 7 error(s) found in file!

# Metadata

File size: 9 bytes
Checkers: ['python_ags4 v0.5.0']
Dictionary: Standard_dictionary_v4_1_1.ags
Time: 2021-08-23 14:25:43+00:00


# Errors

## AGS Format Rule 2a

Line: 1 - Is not terminated by <CR> and <LF> characters.

## AGS Format Rule 3

Line: 1 - Does not start with a valid data descriptor.

## AGS Format Rule 5

Line: 1 - Contains fields that are not enclosed in double quotes.

## AGS Format Rule 13

Group: PROJ - PROJ group not found.

## AGS Format Rule 14

Group: TRAN - TRAN group not found.

## AGS Format Rule 15

Group: UNIT - UNIT group not found.

## AGS Format Rule 17

Group: TYPE - TYPE group not found.

================================================================================
""",
    'random_binary.ags': """
================================================================================
random_binary.ags: 37 error(s) found in file!

# Metadata

File size: 1024 bytes
Checkers: ['python_ags4 v0.5.0']
Dictionary: Standard_dictionary_v4_1_1.ags
Time: 2021-08-23 14:25:43+00:00


# Errors

## AGS Format Rule 1

Line: 1 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8') and/or a byte-order-mark (BOM).
Line: 2 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 3 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 4 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 5 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 6 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 7 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').
Line: 8 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8').

## AGS Format Rule 13

Group: PROJ - PROJ group not found.

## AGS Format Rule 14

Group: TRAN - TRAN group not found.

## AGS Format Rule 15

Group: UNIT - UNIT group not found.

## AGS Format Rule 17

Group: TYPE - TYPE group not found.

## AGS Format Rule 2a

Line: 1 - Is not terminated by <CR> and <LF> characters.
Line: 2 - Is not terminated by <CR> and <LF> characters.
Line: 3 - Is not terminated by <CR> and <LF> characters.
Line: 4 - Is not terminated by <CR> and <LF> characters.
Line: 5 - Is not terminated by <CR> and <LF> characters.
Line: 6 - Is not terminated by <CR> and <LF> characters.
Line: 7 - Is not terminated by <CR> and <LF> characters.
Line: 8 - Is not terminated by <CR> and <LF> characters.

## AGS Format Rule 3

Line: 1 - Does not start with a valid data descriptor.
Line: 2 - Does not start with a valid data descriptor.
Line: 3 - Does not start with a valid data descriptor.
Line: 4 - Does not start with a valid data descriptor.
Line: 5 - Does not start with a valid data descriptor.
Line: 6 - Does not start with a valid data descriptor.
Line: 7 - Does not start with a valid data descriptor.
Line: 8 - Does not start with a valid data descriptor.

## AGS Format Rule 5

Line: 1 - Contains fields that are not enclosed in double quotes.
Line: 2 - Contains fields that are not enclosed in double quotes.
Line: 3 - Contains fields that are not enclosed in double quotes.
Line: 4 - Contains fields that are not enclosed in double quotes.
Line: 5 - Contains fields that are not enclosed in double quotes.
Line: 6 - Contains fields that are not enclosed in double quotes.
Line: 7 - Contains fields that are not enclosed in double quotes.
Line: 8 - Contains fields that are not enclosed in double quotes.

## General

Line:  - AGS4 Rule 1 is interpreted as allowing both standard ASCII characters (Unicode code points 0-127) and extended ASCII characters (Unicode code points 160-255). Please beware that extended ASCII characters differ based on the encoding used when the file was created. The validator defaults to 'utf-8' encoding as it is the most widely used encoding compatible with Unicode. The user can override this default if the file encoding is different but, it is highly recommended that the 'utf-8' encoding be used when creating AGS4 files. (Hint: If not 'utf-8', then the encoding is most likely to be 'windows-1252' aka 'cp1252')

================================================================================
""",
    'real/Blackburn Southern Bypass.ags': """
================================================================================
Blackburn Southern Bypass.ags: 95 error(s) found in file!

# Metadata

File size: 6566 bytes
Checkers: ['python_ags4 v0.5.0']
Dictionary: Standard_dictionary_v4_1_1.ags
Time: 2021-08-23 14:25:43+00:00


# Errors

## AGS Format Rule 1

Line: 1 - Has Non-ASCII character(s) (assuming that file encoding is 'utf-8') and/or a byte-order-mark (BOM).

## AGS Format Rule 2a

Line: 1 - Is not terminated by <CR> and <LF> characters.
Line: 2 - Is not terminated by <CR> and <LF> characters.
Line: 3 - Is not terminated by <CR> and <LF> characters.
Line: 4 - Is not terminated by <CR> and <LF> characters.
Line: 5 - Is not terminated by <CR> and <LF> characters.
Line: 6 - Is not terminated by <CR> and <LF> characters.
Line: 7 - Is not terminated by <CR> and <LF> characters.
Line: 8 - Is not terminated by <CR> and <LF> characters.
Line: 9 - Is not terminated by <CR> and <LF> characters.
Line: 10 - Is not terminated by <CR> and <LF> characters.
Line: 11 - Is not terminated by <CR> and <LF> characters.
Line: 12 - Is not terminated by <CR> and <LF> characters.
Line: 13 - Is not terminated by <CR> and <LF> characters.
Line: 14 - Is not terminated by <CR> and <LF> characters.
Line: 15 - Is not terminated by <CR> and <LF> characters.
Line: 16 - Is not terminated by <CR> and <LF> characters.
Line: 17 - Is not terminated by <CR> and <LF> characters.
Line: 18 - Is not terminated by <CR> and <LF> characters.
Line: 19 - Is not terminated by <CR> and <LF> characters.
Line: 20 - Is not terminated by <CR> and <LF> characters.
Line: 21 - Is not terminated by <CR> and <LF> characters.
Line: 22 - Is not terminated by <CR> and <LF> characters.
Line: 23 - Is not terminated by <CR> and <LF> characters.
Line: 24 - Is not terminated by <CR> and <LF> characters.
Line: 25 - Is not terminated by <CR> and <LF> characters.
Line: 26 - Is not terminated by <CR> and <LF> characters.
Line: 27 - Is not terminated by <CR> and <LF> characters.
Line: 28 - Is not terminated by <CR> and <LF> characters.
Line: 29 - Is not terminated by <CR> and <LF> characters.
Line: 30 - Is not terminated by <CR> and <LF> characters.
Line: 31 - Is not terminated by <CR> and <LF> characters.
Line: 32 - Is not terminated by <CR> and <LF> characters.
Line: 33 - Is not terminated by <CR> and <LF> characters.
Line: 34 - Is not terminated by <CR> and <LF> characters.
Line: 35 - Is not terminated by <CR> and <LF> characters.
Line: 36 - Is not terminated by <CR> and <LF> characters.
Line: 37 - Is not terminated by <CR> and <LF> characters.
Line: 38 - Is not terminated by <CR> and <LF> characters.
Line: 39 - Is not terminated by <CR> and <LF> characters.
Line: 40 - Is not terminated by <CR> and <LF> characters.
Line: 41 - Is not terminated by <CR> and <LF> characters.
Line: 42 - Is not terminated by <CR> and <LF> characters.
Line: 43 - Is not terminated by <CR> and <LF> characters.
Line: 44 - Is not terminated by <CR> and <LF> characters.
Line: 45 - Is not terminated by <CR> and <LF> characters.
Line: 46 - Is not terminated by <CR> and <LF> characters.
Line: 47 - Is not terminated by <CR> and <LF> characters.
Line: 48 - Is not terminated by <CR> and <LF> characters.
Line: 49 - Is not terminated by <CR> and <LF> characters.
Line: 50 - Is not terminated by <CR> and <LF> characters.
Line: 51 - Is not terminated by <CR> and <LF> characters.
Line: 52 - Is not terminated by <CR> and <LF> characters.
Line: 53 - Is not terminated by <CR> and <LF> characters.
Line: 54 - Is not terminated by <CR> and <LF> characters.
Line: 55 - Is not terminated by <CR> and <LF> characters.
Line: 56 - Is not terminated by <CR> and <LF> characters.
Line: 57 - Is not terminated by <CR> and <LF> characters.
Line: 58 - Is not terminated by <CR> and <LF> characters.
Line: 59 - Is not terminated by <CR> and <LF> characters.
Line: 60 - Is not terminated by <CR> and <LF> characters.
Line: 61 - Is not terminated by <CR> and <LF> characters.
Line: 62 - Is not terminated by <CR> and <LF> characters.
Line: 63 - Is not terminated by <CR> and <LF> characters.
Line: 64 - Is not terminated by <CR> and <LF> characters.
Line: 65 - Is not terminated by <CR> and <LF> characters.
Line: 66 - Is not terminated by <CR> and <LF> characters.
Line: 67 - Is not terminated by <CR> and <LF> characters.
Line: 68 - Is not terminated by <CR> and <LF> characters.
Line: 69 - Is not terminated by <CR> and <LF> characters.
Line: 70 - Is not terminated by <CR> and <LF> characters.
Line: 71 - Is not terminated by <CR> and <LF> characters.
Line: 72 - Is not terminated by <CR> and <LF> characters.
Line: 73 - Is not terminated by <CR> and <LF> characters.
Line: 74 - Is not terminated by <CR> and <LF> characters.
Line: 75 - Is not terminated by <CR> and <LF> characters.
Line: 76 - Is not terminated by <CR> and <LF> characters.
Line: 77 - Is not terminated by <CR> and <LF> characters.
Line: 78 - Is not terminated by <CR> and <LF> characters.
Line: 79 - Is not terminated by <CR> and <LF> characters.
Line: 80 - Is not terminated by <CR> and <LF> characters.
Line: 81 - Is not terminated by <CR> and <LF> characters.
Line: 82 - Is not terminated by <CR> and <LF> characters.
Line: 83 - Is not terminated by <CR> and <LF> characters.
Line: 84 - Is not terminated by <CR> and <LF> characters.
Line: 85 - Is not terminated by <CR> and <LF> characters.
Line: 86 - Is not terminated by <CR> and <LF> characters.
Line: 87 - Is not terminated by <CR> and <LF> characters.
Line: 88 - Is not terminated by <CR> and <LF> characters.
Line: 89 - Is not terminated by <CR> and <LF> characters.
Line: 90 - Is not terminated by <CR> and <LF> characters.

## AGS Format Rule 3

Line: 1 - Does not start with a valid data descriptor.

## AGS Format Rule 5

Line: 1 - Contains fields that are not enclosed in double quotes.

## General

Line:  - AGS4 Rule 1 is interpreted as allowing both standard ASCII characters (Unicode code points 0-127) and extended ASCII characters (Unicode code points 160-255). Please beware that extended ASCII characters differ based on the encoding used when the file was created. The validator defaults to 'utf-8' encoding as it is the most widely used encoding compatible with Unicode. The user can override this default if the file encoding is different but, it is highly recommended that the 'utf-8' encoding be used when creating AGS4 files. (Hint: If not 'utf-8', then the encoding is most likely to be 'windows-1252' aka 'cp1252')
Line:  - This file seems to be encoded with a byte-order-mark (BOM). It is highly recommended that the file be saved without BOM encoding to avoid issues with other software.

================================================================================
"""
}
