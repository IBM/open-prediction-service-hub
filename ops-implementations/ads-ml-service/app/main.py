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
import pathlib
import tempfile

import fastapi
import fastapi.responses as responses
import yaml

LOGGER = logging.getLogger(__name__)


def get_app() -> fastapi.FastAPI:
    import app.api.api_v2.api as api_v2
    import app.core.configuration as app_conf
    import app.version as ads_ml_service_version

    app = fastapi.FastAPI(
        version=ads_ml_service_version.__version__,
        title='ADS ML Service',
        description='A simple Machine Learning serving environment for tests',
        openapi_url='/open-prediction-service.json',
        default_response_class=responses.ORJSONResponse,
        debug=True
    )

    @app.on_event("startup")
    async def startup():
        conf = yaml.safe_load(app_conf.get_config().LOGGING.read_text())
        debug_mode = app_conf.get_config().DEBUG
        if debug_mode:
            for _, logger_config in conf['loggers'].items():
                logger_config['level'] = 'DEBUG'
        logging.config.dictConfig(conf)
        if debug_mode:
            LOGGER.info("Launching application in debug mode")

    @app.get(path='/', include_in_schema=False)
    async def redirect_docs() -> responses.RedirectResponse:
        return responses.RedirectResponse(url='/docs')

    app.include_router(api_v2.api_router)
    return app


def launch_test_server():
    import asyncio

    import hypercorn.config as h_config
    import hypercorn.asyncio as h_asyncio

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        current = pathlib.Path(__file__).parent

        logging_configs = yaml.safe_load((current / '..' / 'logging.yaml').read_text())
        logging_configs['handlers']['info_file_handler']['filename'] = str(root / 'info.log')
        logging_configs['handlers']['error_file_handler']['filename'] = str(root / 'error.log')
        os.environ['LOGGING'] = str(root / 'logging.yaml')
        os.environ['DEBUG'] = str(True)
        os.environ['SETTINGS'] = str(root)
        os.environ['MODEL_STORAGE'] = str(root)
        (root / 'logging.yaml').write_text(yaml.dump(logging_configs))

        app = get_app()
        hypercorn_config = h_config.Config()
        hypercorn_config.bind = ["localhost:8080"]
        asyncio.run(h_asyncio.serve(app, hypercorn_config))


if __name__ == '__main__':
    launch_test_server()
