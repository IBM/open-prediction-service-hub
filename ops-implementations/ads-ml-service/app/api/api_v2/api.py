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


import fastapi

import app.api.api_v2.endpoints.capabilities as capabilities
import app.api.api_v2.endpoints.endpoints as endpoints
import app.api.api_v2.endpoints.info as info
import app.api.api_v2.endpoints.login as login
import app.api.api_v2.endpoints.models as models
import app.api.api_v2.endpoints.predictions as predictions
import app.api.api_v2.endpoints.users as users
import app.api.api_v2.endpoints.upload as upload

api_router = fastapi.APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['account'])
api_router.include_router(login.router, tags=['login'])
api_router.include_router(info.router, tags=['info'])
api_router.include_router(capabilities.router, tags=['info'])
api_router.include_router(models.router)
api_router.include_router(upload.router)
api_router.include_router(endpoints.router)
api_router.include_router(predictions.router, tags=['run'])
