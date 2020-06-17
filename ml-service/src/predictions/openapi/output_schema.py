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

from enum import Enum
from typing import Text, List

from pydantic import BaseModel, Field


class OutputType(str, Enum):
    INT: Text = 'int'
    FLOAT: Text = 'float'
    STRING: Text = 'string'
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
