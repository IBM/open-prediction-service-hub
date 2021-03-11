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

import fastapi

import app.gen.schemas.ops_schemas as ops_model

router = fastapi.APIRouter()


@router.get(
    path='/capabilities',
    response_model=ops_model.Capabilities
)
async def server_capabilities() -> typing.Dict[typing.Text, typing.Any]:
    return {
        'capabilities': [
            ops_model.Capability.info,
            ops_model.Capability.discover,
            ops_model.Capability.manage,
            ops_model.Capability.run
        ],
        'managed_capabilities': {
            'supported_input_data_structure': ['auto', 'DataFrame', 'ndarray', 'DMatrix', 'list'],
            'supported_output_data_structure': ['auto', 'DataFrame', 'ndarray', 'list'],
            'supported_format': ['pickle', 'joblib', 'pmml', 'bst']
        }
    }
