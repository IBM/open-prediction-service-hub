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


import datetime as dt
import typing

import pydantic as pyd


class ModelBase(pyd.BaseModel):
    name: typing.Optional[typing.Text] = None


class ModelCreate(ModelBase):
    name: typing.Text


class ModelUpdate(ModelBase):
    pass


class ModelInDBBase(ModelBase):
    id: int
    name: typing.Text
    created_at: dt.datetime
    modified_at: dt.datetime

    class Config:
        orm_mode = True


class Model(ModelInDBBase):
    pass


class ModelInDB(ModelInDBBase):
    pass
