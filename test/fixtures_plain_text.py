PLAIN_TEXT_RESPONSES = {
    'example_ags.ags': """
example_ags.ags: All checks passed!

# Metadata

File size: 4039 bytes
Checker: python_ags4 v0.3.6
Dictionary: Standard_dictionary_v4_1.ags
Time: 2021-08-23 14:25:43+00:00
""",
    'nonsense.ags': """
nonsense.ags: 7 error(s) found in file!

# Metadata

File size: 9 bytes
Checker: python_ags4 v0.3.6
Dictionary: Standard_dictionary_v4_1.ags
Time: 2021-08-23 14:25:43+00:00

# Errors

## Rule 2a

Line: 1 - Is not terminated by <CR> and <LF> characters.

## Rule 3

Line: 1 - Does not start with a valid data descriptor.

## Rule 5

Line: 1 - Contains fields that are not enclosed in double quotes.

## Rule 13

Group: PROJ - PROJ table not found.

## Rule 14

Group: TRAN - TRAN table not found.

## Rule 15

Group: UNIT - UNIT table not found.

## Rule 17

Group: TYPE - TYPE table not found.
""",
    'random_binary.ags': """
random_binary.ags: 1 error(s) found in file!

# Metadata

File size: 1024 bytes
Checker: python_ags4 v0.3.6
Time: 2021-08-23 14:25:43+00:00

# Errors

## UnicodeDecodeError

Line: 1 - invalid continuation byte
""",
    'real/Blackburn Southern Bypass.ags': """
Blackburn Southern Bypass.ags: 93 error(s) found in file!

# Metadata

File size: 6566 bytes
Checker: python_ags4 v0.3.6
Time: 2021-08-23 14:25:43+00:00

# Errors

## Rule 1

Line: 1 - Has Non-ASCII character(s).

## Rule 2a

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

## Rule 3

Line: 1 - Does not start with a valid data descriptor.

## Rule 5

Line: 1 - Contains fields that are not enclosed in double quotes.
"""
}
