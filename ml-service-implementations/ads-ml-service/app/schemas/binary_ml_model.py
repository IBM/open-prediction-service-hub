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


import typing

import pydantic as pyd

import app.schemas.mapping as mapping


class BinaryMlModelBase(pyd.BaseModel):
    model_b64: typing.Optional[bytes] = None
    input_handling: typing.Optional[mapping.ModelInput] = None
    output_handling: typing.Optional[mapping.ModelOutput] = None
    loader: typing.Optional[mapping.ModelLoader] = None


class BinaryMlModelCreate(BinaryMlModelBase):
    model_b64: bytes
    input_handling: mapping.ModelInput
    output_handling: mapping.ModelOutput
    loader: mapping.ModelLoader


class BinaryMlModelUpdate(BinaryMlModelBase):
    pass


class BinaryMlModelInDBBase(BinaryMlModelBase):
    id: int
    model_b64: bytes
    input_handling: mapping.ModelInput
    output_handling: mapping.ModelOutput
    loader: mapping.ModelLoader
    endpoint_id: int

    class Config:
        orm_mode = True


class BinaryMlModel(BinaryMlModelInDBBase):
    pass


class BinaryMlModelInDB(BinaryMlModelInDBBase):
    pass
