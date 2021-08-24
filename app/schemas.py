from datetime import datetime
from enum import Enum
from typing import Dict, List, Union

from pydantic import BaseModel, Field


class GroupEnum(str, Enum):
    proj = 'PROJ'
    tran = 'TRAN'
    unit = 'UNIT'
    type_ = 'TYPE'
    none = ''


class LineError(BaseModel):
    line: str = Field(..., example="5")
    group: GroupEnum = Field(..., example="TRAN")
    desc: str = Field(..., example="Blah blah")


class Validation(BaseModel):
    filename: str = Field(..., example="example.ags")
    filesize: int = Field(None, example="1024")
    checker: str = Field(None, example="python_ags4 v0.3.6")
    dictionary: str = Field(None, example="Standard_dictionary_v4_1.ags")
    time: datetime = Field(None, example="2021-08-18 09:23:29")
    message: str = Field(None, example="7 error(s) found in file!")
    errors: Dict[str, List[LineError]]  = Field(..., example="Rule 1a")


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
