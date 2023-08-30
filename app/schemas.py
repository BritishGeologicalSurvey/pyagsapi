from datetime import datetime
from typing import Dict, List, Union

from pydantic import BaseModel, Field, validator

from app.bgs_rules import BGS_RULES

VALID_KEYS = [
    # AGS schema rules
    'AGS Format Rule 1', 'AGS Format Rule 2', 'AGS Format Rule 2a', 'AGS Format Rule 2b',
    'AGS Format Rule 2c', 'AGS Format Rule 3', 'AGS Format Rule 4a', 'AGS Format Rule 4b',
    'AGS Format Rule 5', 'AGS Format Rule 6', 'AGS Format Rule 7', 'AGS Format Rule 8',
    'AGS Format Rule 9', 'AGS Format Rule 10a', 'AGS Format Rule 10b', 'AGS Format Rule 10c',
    'AGS Format Rule 11a', 'AGS Format Rule 11b', 'AGS Format Rule 11c', 'AGS Format Rule 12',
    'AGS Format Rule 13', 'AGS Format Rule 14', 'AGS Format Rule 15', 'AGS Format Rule 16',
    'AGS Format Rule 17', 'AGS Format Rule 18', 'AGS Format Rule 19', 'AGS Format Rule 19a',
    'AGS Format Rule 19b', 'AGS Format Rule 20', 'General',
    # Errors
    'File read error'
]
# Add BGS data rules
VALID_KEYS.extend(list(BGS_RULES.keys()))
# BGS rule that is handled outside of the rule functions
VALID_KEYS.append('BGS data validation: Non-numeric coordinate types')


class LineError(BaseModel):
    line: Union[int, str] = Field(..., example="5")
    group: str = Field(..., example="TRAN")
    desc: str = Field(..., example="Blah blah")

    @validator('line')
    def line_if_string_must_be_hyphen(cls, line):
        if type(line) is str:
            assert line in ['-', ''], f"Unknown non-integer line number: '{line}'"
        return line


class Validation(BaseModel):
    filename: str = Field(..., example="example.ags")
    filesize: int = Field(None, example="1024")
    checkers: List[str] = Field(None, example=["python_ags4 v0.4.1"])
    dictionary: str = Field(None, example="Standard_dictionary_v4_1_1.ags")
    time: datetime = Field(None, example="2021-08-18 09:23:29")
    message: str = Field(None, example="7 error(s) found in file!")
    errors: Dict[str, List[LineError]] = Field(..., example="Rule 1a")
    valid: bool = Field(..., example='false')
    additional_metadata: dict = Field(...)

    @validator('errors')
    def errors_keys_must_be_known_rules(cls, errors):
        for key in errors.keys():
            assert key in VALID_KEYS, f"Unknown rule: '{key}'"
        return errors


class Error(BaseModel):
    error: str = Field(..., example="error")
    propName:  str = Field(None, example="error")
    desc: str = Field(..., example="Error message")


class MinimalResponse(BaseModel):
    msg: str = Field(..., example="Example response")
    type: str = Field(..., example="success")
    self: str = Field(..., example="http://example.com/apis/query")


class ErrorResponse(MinimalResponse):
    errors: List[Error] = None


class ValidationResponse(MinimalResponse):
    data: List[Union[Validation, bool]] = None


class BoreholeCountResponse(MinimalResponse):
    count: int = Field(..., example=4)
