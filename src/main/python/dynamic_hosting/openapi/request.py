#!/usr/bin/env python3

from __future__ import annotations

from typing import Text, Dict, Union, Any, List, Type

from pydantic import BaseModel, Field

# Union[int, float, str] The support of polymorphic input is not released
# (https://github.com/OpenAPITools/openapi-generator/pull/5120)
FEAT_VAL_T: Type = str


class Parameter(BaseModel):
    """Parameter for ml model invocation"""
    name: Text = Field(..., description='Name of the feature')
    value: FEAT_VAL_T = Field(..., description='Value of the feature')

    def get_feature_name(self) -> Text:
        return self.name

    def get_feature_value(self) -> FEAT_VAL_T:
        return self.value


class RequestBody(BaseModel):
    """RequestBody captures all information needed for model invocation"""
    model_name: Text = Field(..., description='Name of model')
    model_version: Text = Field(..., description='Version of model')
    params: List[Parameter] = Field(..., description='Model parameters')

    def get_model_name(self) -> Text:
        return self.model_name

    def get_model_version(self) -> Text:
        return self.model_version

    def get_parameters(self) -> List[Parameter]:
        return self.params

    def get_data(self) -> Dict[Text, FEAT_VAL_T]:
        return {
            parameter.get_feature_name(): parameter.get_feature_value()
            for parameter in self.get_parameters()
        }
