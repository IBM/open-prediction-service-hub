import logging
import sys
from typing import Callable, Text, Mapping, Type, List, Union, Tuple

import uvicorn
from dynamic_hosting.core.openapi.model import ResponseBody, Model
from dynamic_hosting.core.openapi.request import GenericRequestBody, DirectRequestBody, RequestMetadata
from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.core.util import find_storage_root, load_direct_request_schema, replace_any_of
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.utils import get_model_definitions
from pydantic import BaseModel, create_model

app = FastAPI(
    version='0.0.1-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model',
    docs_url='/'
)


def model_name_map_gen(model_types: Tuple[Type[BaseModel]]) -> Mapping[Type, Text]:
    return {c: c.__name__ for c in model_types}


def dynamic_io_schema_gen(ms: ModelService) -> Callable:
    def dynamic_io_schema():
        ms.reload_models()
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        input_schema_models: Tuple[Type[BaseModel]] = tuple()
        for model in ms.ml_models:
            openapi_schema['components']['schemas'].update(
                model.input_schema_definition()
            )
            input_schema_models += (model.input_schema_model(), )

        m = create_model(
            'Dynamic{class_name}'.format(class_name=DirectRequestBody.__name__),
            dynamic_params=(Union[tuple(input_schema_models)], ...),
            __base__=DirectRequestBody
        )

        real_request_class_name: Text = 'Dynamic{class_name}'.format(class_name=DirectRequestBody.__name__)

        d = get_model_definitions(
            flat_models={m, *input_schema_models},
            model_name_map={m: real_request_class_name,
                            **model_name_map_gen(input_schema_models),
                            RequestMetadata: 'RequestMetadata'}

        )

        openapi_schema['components']['schemas'].update(
            d
        )

        load_direct_request_schema(openapi_schema['paths']['/direct'], DirectRequestBody.__name__, real_request_class_name)

        replace_any_of(openapi_schema['components']['schemas'], real_request_class_name, 'dynamic_params')

        return openapi_schema

    return dynamic_io_schema


@app.get('/isAlive', response_model=Mapping)
def heart_beat() -> Mapping:
    return {'status': 'good'}


@app.get('/models', response_model=ModelService)
def get_models() -> ModelService:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    return ms


@app.post('/models')
def add_model(m: Model) -> None:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    ms.add_model(m)


@app.delete('/models')
def remove_model(model_name: Text, model_version: Text = None) -> None:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    ms.remove_model(model_name=model_name, model_version=model_version)


@app.post('/generic', response_model=ResponseBody)
def predict(ml_req: GenericRequestBody) -> ResponseBody:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    internal_res = ms.invoke_from_dict(
        model_name=ml_req.metadata.model_name,
        model_version=ml_req.metadata.model_version,
        data=ml_req.get_dict()
    )
    return ResponseBody(
        model_output_raw=str(internal_res)
    )


@app.post('/direct', response_model=ResponseBody)
def predict(ml_req: DirectRequestBody) -> ResponseBody:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())
    internal_res = ms.invoke_from_dict(
        model_name=ml_req.get_model_name(),
        model_version=ml_req.get_version(),
        data=ms.model_map()[ml_req.get_model_name()][ml_req.get_version()].transform_internal_dict(ml_req)
    )
    return ResponseBody(
        model_output_raw=str(internal_res)
    )


app.openapi = dynamic_io_schema_gen(ms=ModelService.load_from_disk(find_storage_root()))

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000)
