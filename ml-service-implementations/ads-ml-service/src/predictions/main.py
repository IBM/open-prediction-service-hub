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


from typing import Text

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from predictions.api.api_v1.api import api_router


__version__: str = '0.1.0'

app: FastAPI = FastAPI(
    version=__version__,
    title='Open Prediction Service',
    description='A simple Machine Learning serving environment for tests',
    openapi_url="/open-prediction-service.json"
)

VER: int = 1
PREFIX: Text = f'/v{VER}'

app.include_router(api_router, prefix=PREFIX)


@app.get(
    path=f'{PREFIX}/docs', include_in_schema=False
)
def redirect_docs():
    return RedirectResponse(url='/docs')


@app.get(
    path='/', include_in_schema=False
)
def redirect_docs():
    return RedirectResponse(url='/docs')
