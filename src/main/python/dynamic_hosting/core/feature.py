#!/usr/bin/env python3

from __future__ import annotations

from typing import Text, Type, Any

import numpy
from pydantic import BaseModel, Field, validator


def _check_type(obj: Any, expected_type: Type) -> Any:
    if isinstance(obj, expected_type):
        return obj
    else:
        ValueError(
            'Feature type expected to be {ex} but received {re}'.format(ex=str(expected_type), re=str(type(obj))))


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
        if t in ('int', 'float', 'str'):
            return t
        if getattr(numpy, t) and numpy.issubdtype(t, numpy.generic):
            return t
        else:
            raise ValueError('Type not supported: {t}'.format(t=t))

    def get_name(self) -> Text:
        return self.name

    def get_type(self) -> Type:
        if self.type in ('int', 'float', 'str'):
            if self.type == 'int:':
                return int
            elif self.type == 'float:':
                return float
            else:
                return str
        else:
            return getattr(numpy, self.type)

    def get_openapi_type(self) -> Type:
        """
        :return: type that can be interpreted into json schema
        """
        t: Type = self.get_type()
        if t in (int, float, str):
            return t
        elif numpy.issubdtype(t, numpy.number):
            return float
        elif numpy.issubdtype(t, numpy.character):
            return str
        else:
            raise ValueError('Unsupported openapi type: {t}'.format(t=t))

    def get_type_validator(self) -> classmethod:
        if self.type in ('int', 'float', 'str'):
            if self.type == 'int:':
                @validator(self.name, pre=False, always=True, allow_reuse=True)
                def is_py_int(obj: Any) -> int:
                    return _check_type(obj=obj, expected_type=int)
                return is_py_int
            elif self.type == 'float:':
                @validator(self.name, pre=False, always=True, allow_reuse=True)
                def is_py_float(obj: Any) -> float:
                    return _check_type(obj=obj, expected_type=float)
                return is_py_float
            else:
                @validator(self.name, pre=False, always=True, allow_reuse=True)
                def is_py_string(obj: Any) -> Text:
                    return _check_type(obj=obj, expected_type=Text)
                return is_py_string
        else:
            @validator(self.name, pre=False, always=True, allow_reuse=True)
            def is_numpy_type(obj: Any) -> numpy.generic:
                return _check_type(obj=obj, expected_type=numpy.generic)
            return is_numpy_type

