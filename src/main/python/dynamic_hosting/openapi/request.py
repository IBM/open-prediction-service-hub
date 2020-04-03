#!/usr/bin/env python3

from __future__ import annotations

from typing import Text, Dict, Union, Any, List

import numpy as np
from pydantic import BaseModel, Field
from pydantic.errors import PydanticTypeError


class Parameter(BaseModel):
    """Parameter for ml model invocation"""
    name: Text = Field(..., description='Name of the feature')
    order: int = Field(..., description='Position of the feature')
    value: Union[np.str, np.long, np.float] = Field(..., description='Value of the feature')


class RequestBody(BaseModel):
    """RequestBody captures all information needed for model invocation"""
    model_name: Text = Field(..., description='Name of model')
    model_version: Text = Field(..., description='Version of model')
    params: Any = Field(..., description='Placeholder for dynamic generated parameter dict')

    def get_model_name(self) -> Text:
        return self.model_name

    def get_model_version(self) -> Text:
        return self.model_version

    def get_parameters(self) -> List[Parameter]:
        try:
            return [
                Parameter(name=name, order=order, value=value)
                for order, (name, value) in enumerate(getattr(self, 'params').dict().items())
            ]
        except PydanticTypeError:
            raise RuntimeError('Can not cast received data into ml input format')

    def get_data(self) -> Dict[Text, List[Any]]:
        return {
            getattr(parameter, 'name'): getattr(parameter, 'value')
            for parameter in self.get_parameters()
        }
