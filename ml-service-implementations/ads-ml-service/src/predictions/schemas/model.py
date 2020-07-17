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

from typing import Text, Optional, Sequence, Dict

from pydantic import BaseModel, Field

from .feature import Feature
from .metadata import Metadata
from .output_schema import OutputSchema
from ..schemas.binary_ml_model import BinaryMLModelBase, BinaryMLModelCreate
from ..schemas.model_config import ModelConfigBase, ModelConfigCreate


class MLSchema(BaseModel):
    """Model independent information"""
    name: Text = Field(..., description='Name of model')
    version: Text = Field(..., description='Version of model')
    method_name: Text = Field(..., description='Name of method. (e.g predict, predict_proba)')
    input_schema: Sequence[Feature] = Field(..., description='Input schema of ml model')
    output_schema: Optional[OutputSchema] = Field(..., description='Output schema of ml model')
    metadata: Metadata = Field(..., description='Additional information for ml model')


# Shared properties
class ModelBase(BaseModel):
    name: Optional[Text] = None
    version: Optional[Text] = None
    binary: Optional[BinaryMLModelBase] = None
    config: Optional[ModelConfigBase] = None


# Properties to receive via API on creation
class ModelCreate(ModelBase):
    name: Text
    version: Text
    binary: Optional[BinaryMLModelCreate] = None
    config: Optional[ModelConfigCreate] = None


# Properties to receive via API on update
class ModelUpdate(ModelBase):
    pass


class ModelInDBBase(ModelBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Model(ModelInDBBase):
    pass


# Additional properties to be storied in DB
class ModelInDB(ModelInDBBase):
    pass
