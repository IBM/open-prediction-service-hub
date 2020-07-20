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


from typing import Text, Optional, Dict, List

from pydantic import BaseModel, Field


class Metric(BaseModel):
    name: Text = Field(..., description='Name of metric')
    value: Text = Field(..., description='Value of metric')


class Metadata(BaseModel):
    description: Text = Field(..., description='Description of model')
    author: Text = Field(..., description='Author of model')
    trained_at: Text = Field(..., description='Training date')
    class_names: Optional[Dict[int, Text]] = Field(
        None, description='Lookup table for class index <-> class name'
    )
    metrics: List[Metric] = Field(..., description='Metrics for model')
