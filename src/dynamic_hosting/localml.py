import logging
import sys
from typing import Callable, Text

import uvicorn
from dynamic_hosting.core.model import MLRequest, MLResponse, MLModel
from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.core.util import find_storage_root
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

app = FastAPI(
    version='0.0.1-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model',
    docs_url='/'
)


def dynamic_io_schema_gen(ms: ModelService) -> Callable:
    def dynamic_io_schema():
        ms.reload_models()
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        openapi_schema['components']['schemas'].update(
            {
                '{name}-{version}'.format(
                    name=model.name, version=model.version
                ): model.additional_input_schema.dict()
                for model in ms.ml_models
            }
        )
        openapi_schema['components']['test'] = {}
        return openapi_schema
    return dynamic_io_schema


class ServerStatus(BaseModel):
    status: str = 'bad'


@app.get('/isAlive', response_model=ServerStatus)
def heart_beat() -> ServerStatus:
    return ServerStatus(status='good')


@app.get('/models', response_model=ModelService)
def get_models() -> ModelService:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    return ms


@app.post('/models')
def add_model(m: MLModel) -> None:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    ms.add_model(m)


@app.delete('/models')
def remove_model(model_name: Text, model_version: Text = None) -> None:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    ms.remove_model(model_name=model_name, model_version=model_version)


@app.post('/generic', response_model=MLResponse)
def predict(ml_req: MLRequest) -> MLResponse:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    internal_res = ms.invoke_from_dict(
        model_name=ml_req.model_name,
        model_version=ml_req.model_version,
        data=MLRequest.params_to_dict(ml_req)
    )
    return MLResponse(
        model_output_raw=str(internal_res)
    )


app.openapi = dynamic_io_schema_gen(ms=ModelService.load_from_disk(find_storage_root()))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000)
