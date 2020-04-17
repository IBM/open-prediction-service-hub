#!/usr/bin/env python3

from __future__ import annotations

from typing import Text, Type

import numpy
from pydantic import BaseModel, Field, validator


class Feature(BaseModel):
    """
    Feature of machine learning model
    :param name: name of the feature
    :param order: the position of the feature in method signature
    :param type: type of feature. Can be python type or numpy type
    """
    name: Text = Field(..., description='Feature name')
    order: int = Field(..., description='Position of feature')
    type: Text = Field(..., description='Numpy type of feature')

    class Config:
        """Feature is immutable inside model"""
        allow_mutation: bool = False

    @validator('type', always=True)
    def type_check(cls, t) -> Type:
        if t in ('int', 'float', 'bool', 'str'):  # Python type
            return t
        if hasattr(numpy, t) and numpy.issubdtype(t, numpy.generic):
            return t
        else:
            raise ValueError('Type not supported: {t}'.format(t=t))

    def get_type(self) -> Type:
        if self.type in ('int', 'float', 'bool', 'str'):
            if self.type == 'int':
                return int
            elif self.type == 'float':
                return float
            elif self.type == 'bool':
                return bool
            else:
                return str
        else:
            return getattr(numpy, self.type)
