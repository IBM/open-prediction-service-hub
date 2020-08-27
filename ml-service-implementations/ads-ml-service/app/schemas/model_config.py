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


from typing import Text, Optional, Dict, Any

from pydantic import BaseModel


# Shared properties
class ModelConfigBase(BaseModel):
    configuration: Optional[Dict[Text, Any]]


# Properties to receive via API on creation
class ModelConfigCreate(ModelConfigBase):
    configuration: Dict[Text, Any]


# Properties to receive via API on update
class ModelConfigUpdate(ModelConfigBase):
    pass


class ModelConfigInDBBase(ModelConfigBase):
    id: int
    configuration: Dict[Text, Any]

    class Config:
        orm_mode = True


# Additional properties to return via API
class ModelConfig(ModelConfigInDBBase):
    pass


# Additional properties to be storied in DB
class ModelConfigInDB(ModelConfigInDBBase):
    pass
