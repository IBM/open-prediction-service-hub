#!/usr/bin/env python3


from __future__ import annotations

from enum import Enum
from typing import Text, List

from pydantic import BaseModel, Field


class OutputType(str, Enum):
    INT: Text = 'int'
    FLOAT: Text = 'float'
    BOOL: Text = 'bool'
    STRING: Text = 'str'
    PROBABILITY_ARRAY: Text = "[Probability]"


class OutputAttr(BaseModel):
    name: Text = Field(..., description='Attribute name')
    type: OutputType = Field(..., description='Attribute type')

    class Config:
        """Attribute is immutable"""
        allow_mutation: bool = False

    # def get_type(self) -> Type:
    #     if self.type == OutputType.INT:
    #         return int
    #     elif self.type == OutputType.FLOAT:
    #         return float
    #     elif self.type == OutputType.BOOL:
    #         return bool
    #     elif self.type == OutputType.STRING:
    #         return str
    #     else:
    #         return List[Probability]


class OutputSchema(BaseModel):
    attributes: List[OutputAttr] = Field(...)
