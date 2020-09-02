#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


from __future__ import annotations

from typing import Text, Dict, Union, Any, List, Type

from pydantic import BaseModel, Field

# Union[int, float, str] The support of polymorphic input is not released
# (https://github.com/OpenAPITools/openapi-generator/pull/5120)
FEAT_VAL_T: Type = Text


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
