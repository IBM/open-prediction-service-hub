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


from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api import api_v1
from app.api import api_v2
from app.core.configuration import get_config


from app.version import __version__

app: FastAPI = FastAPI(
    version=__version__,
    title='Open Prediction Service',
    description='A simple Machine Learning serving environment for tests',
    openapi_url="/open-prediction-service.json"
)

app.include_router(api_v1.api.api_router, prefix=get_config().API_V1_STR)
app.include_router(api_v2.api.api_router, prefix=get_config().API_V2_STR)


@app.get(
    path=f'{get_config().API_V1_STR}/docs', include_in_schema=False
)
def redirect_docs():
    return RedirectResponse(url='/docs')


@app.get(
    path=f'{get_config().API_V2_STR}/docs', include_in_schema=False
)
def redirect_docs():
    return RedirectResponse(url='/docs')


@app.get(
    path='/', include_in_schema=False
)
def redirect_docs():
    return RedirectResponse(url='/docs')
