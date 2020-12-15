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


import logging.config
import os

import fastapi
import fastapi.responses as responses
import yaml

import app.api.api_v2.api as api_v2
import app.core.configuration as app_cong
import app.version as ads_ml_service_version


def get_app() -> fastapi.FastAPI:
    with app_cong.get_config().SETTINGS.joinpath('logging.yaml').open(mode='r') as fd:
        conf = yaml.safe_load(fd)
        for _, handler in conf['handlers'].items():
            if 'filename' in handler:
                handler['filename'] = handler['filename'].replace('{{LOG_DIR}}', os.getenv('LOG_DIR'))
        logging.config.dictConfig(conf)

    app = fastapi.FastAPI(
        version=ads_ml_service_version.__version__,
        title='ADS ML Service',
        description='A simple Machine Learning serving environment for tests',
        openapi_url='/open-prediction-service.json',
        default_response_class=responses.ORJSONResponse
    )

    @app.get(path='/', include_in_schema=False)
    async def redirect_docs() -> responses.RedirectResponse:
        return responses.RedirectResponse(url='/docs')

    app.include_router(api_v2.api_router)
    return app
