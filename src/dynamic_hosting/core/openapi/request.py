#!/usr/bin/env python3
from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import Text, Dict, Sequence, Union, Mapping, Any, List

import numpy as np
from pydantic import BaseModel, Field
from pydantic.errors import PydanticTypeError


class RequestMetadata(BaseModel):
    model_name: Text = Field(..., description='Name of model')
    model_version: Text = Field(..., description='Version of model')


class Parameter(BaseModel):
    name: Text = Field(..., description='Name of the feature')
    order: int = Field(..., description='Position of the feature')
    value: Union[np.str, np.long, np.float] = Field(..., description='Value of the feature')


class BaseRequestBody(BaseModel, ABC):
    """Abstract class which captures common information for model invocation"""
    metadata: RequestMetadata = Field(..., alias='metadata', description='Name of this feature')

    def get_model_name(self) -> Text:
        return self.metadata.model_name

    def get_version(self) -> Text:
        return self.metadata.model_version

    @abstractmethod
    def get_parameters(self) -> List[Parameter]:
        pass

    @abstractmethod
    def get_dict(self) -> Dict[Text, Sequence[Any]]:
        pass


class GenericRequestBody(BaseRequestBody):
    """Concrete class which captures necessary information for generic model invocation"""

    params: List[Parameter] = Field(..., description='Input parameters')

    def get_parameters(self) -> List[Parameter]:
        return self.params

    def get_dict(self) -> Dict[Text, Sequence[Any]]:
        return {
            feat_val.name: [feat_val.value]
            for feat_val in self.params
        }


class DirectRequestBody(BaseRequestBody):
    """Concrete class which captures necessary information for direct model invocation"""

    def get_parameters(self) -> List[Parameter]:
        try:
            dynamic_params: BaseModel = getattr(self, 'params')
        except PydanticTypeError:
            raise RuntimeError('Can not cast received data into input format')
        return [
            Parameter(name=i, order=item[0], value=item[1])
            for i, item in enumerate(dynamic_params.__fields__.items())
        ]

    def get_dict(self) -> Dict[Text, Sequence[Any]]:
        return {
            getattr(feat_val, 'name'): [getattr(feat_val, 'value')]
            for feat_val in self.get_parameters()
        }
