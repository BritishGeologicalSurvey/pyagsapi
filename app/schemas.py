from datetime import datetime
from typing import Dict, List, Union

from pydantic import BaseModel, Field, validator

from app.bgs_rules import BGS_RULES

VALID_KEYS = [
    # AGS schema rules
    'Rule 1', 'Rule 2', 'Rule 2a', 'Rule 2b', 'Rule 2c', 'Rule 3', 'Rule 4a', 'Rule 4b',
    'Rule 5', 'Rule 7', 'Rule 9', 'Rule 10a', 'Rule 10b', 'Rule 10c', 'Rule 11a',
    'Rule 11b', 'Rule 11c', 'Rule 13', 'Rule 14', 'Rule 15', 'Rule 16', 'Rule 17',
    'Rule 18', 'Rule 19', 'Rule 19a', 'Rule 19b', 'Rule 19c', 'Rule 20',
    # Errors
    'File read error'
]
# Add BGS data rules
VALID_KEYS.extend(list(BGS_RULES.keys()))
# BGS rule that is handled outside of the rule functions
VALID_KEYS.append('Non-numeric coordinate types')


class LineError(BaseModel):
    line: Union[int, str] = Field(..., example="5")
    group: str = Field(..., example="TRAN")
    desc: str = Field(..., example="Blah blah")

    @validator('line')
    def line_if_string_must_be_hyphen(cls, line):
        if type(line) is str:
            assert line == '-', f"Unknown non-integer line number: '{line}'"
        return line


class Validation(BaseModel):
    filename: str = Field(..., example="example.ags")
    filesize: int = Field(None, example="1024")
    checkers: List[str] = Field(None, example=["python_ags4 v0.3.6"])
    dictionary: str = Field(None, example="Standard_dictionary_v4_1.ags")
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
