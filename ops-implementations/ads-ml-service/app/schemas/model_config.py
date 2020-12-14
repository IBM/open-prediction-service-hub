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

import pydantic


class ModelConfigBase(pydantic.BaseModel):
    configuration: typing.Optional[typing.Dict[typing.Text, typing.Any]]


class ModelConfigCreate(ModelConfigBase):
    configuration: typing.Dict[typing.Text, typing.Any]


class ModelConfigUpdate(ModelConfigBase):
    pass


class ModelConfigInDBBase(ModelConfigBase):
    id: int
    configuration: typing.Dict[typing.Text, typing.Any]
    model_id: int

    class Config:
        orm_mode = True


class ModelConfig(ModelConfigInDBBase):
    pass


class ModelConfigInDB(ModelConfigInDBBase):
    pass
