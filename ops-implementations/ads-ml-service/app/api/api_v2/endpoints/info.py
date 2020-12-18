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
import multiprocessing

import fastapi

import app.gen.schemas.ops_schemas as ops_schemas
import app.version as version

router = fastapi.APIRouter()


@router.get(
    path='/info',
    response_model=ops_schemas.ServerInfo
)
async def server_info() -> typing.Dict[typing.Text, typing.Any]:
    ml_lib_info = {}
    try:
        import sklearn
        import xgboost
        import pypmml
        ml_lib_info = {
            'libraries': {
                'scikit-learn': sklearn.__version__,
                'xgboost': xgboost.__version__,
                'pypmml': pypmml.__version__
            }
        }
    except ImportError:
        sklearn, xgboost, pypmml = None, None, None
    return {
        'info': {
            'server-version': version.__version__,
            'cpu_count': multiprocessing.cpu_count(),
            **ml_lib_info
        },
        'status': ops_schemas.Status2.ok
    }
