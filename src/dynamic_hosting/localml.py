#!/usr/bin/env python3

import logging
import sys
from typing import Callable, Text, Mapping, Type, Tuple, Any

from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.core.openapi.model import ResponseBody, Model
from dynamic_hosting.core.openapi.request import GenericRequestBody, DirectRequestBody, RequestMetadata
from dynamic_hosting.core.util import find_storage_root, load_direct_request_schema, replace_any_of, \
    get_real_request_class
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.utils import get_model_definitions
from pandas import DataFrame
from pydantic import BaseModel, ValidationError

app = FastAPI(
    version='0.0.1-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model',
    docs_url='/'
)

DynamicIOSchemaPrefix = 'Dynamic'


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

        input_request_types: Tuple[Type[BaseModel]] = tuple(ms.input_schema_t_set())
        real_request_class = get_real_request_class(generic_request_class=DirectRequestBody,
                                                    parameter_types=set(input_request_types))

        openapi_schema['components']['schemas'].update(
            get_model_definitions(
                flat_models={real_request_class, *input_request_types},
                model_name_map={real_request_class: real_request_class.__name__,
                                **model_name_map_gen(input_request_types),
                                RequestMetadata: 'RequestMetadata'}
            )
        )

        load_direct_request_schema(
            openapi_schema['paths']['/direct'],
            DirectRequestBody.__name__,
            real_request_class.__name__
        )
        replace_any_of(
            openapi_schema['components']['schemas'],
            real_request_class.__name__,
            'params'
        )

        return openapi_schema

    return dynamic_io_schema


@app.get('/isAlive', response_model=Mapping)
def heart_beat() -> Mapping:
    return {'status': 'good'}


@app.get('/models', response_model=ModelService)
def get_models() -> ModelService:
    """Returns the list of ML models."""
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
    internal_res = ms.invoke(
        model_name=ml_req.metadata.model_name,
        model_version=ml_req.metadata.model_version,
        data=ml_req.get_dict()
    )
    return ResponseBody(
        model_output_raw=str(internal_res)
    )


@app.post('/direct', response_model=ResponseBody)
def predict(
        ml_req: DirectRequestBody
) -> ResponseBody:
    ms: ModelService = ModelService.load_from_disk(find_storage_root())

    # parameterized instantiation
    try:
        concrete_input_model: DirectRequestBody = get_real_request_class(
            generic_request_class=DirectRequestBody,
            parameter_types=ms.input_schema_t_set()
        )(
            metadata=ml_req.metadata,
            params=ml_req.params
        )
    except ValidationError:
        raise HTTPException(status_code=422, detail='ML input mapping failure')

    internal_res: Any = ms.invoke(
        model_name=concrete_input_model.get_model_name(),
        model_version=concrete_input_model.get_version(),
        data=ms.model_map()[concrete_input_model.get_model_name()][
            concrete_input_model.get_version()].transform_internal_dict(concrete_input_model.get_dict())
    )

    return ResponseBody(
        model_output=DataFrame(internal_res).to_dict(orient='list'),
        model_output_raw=str(internal_res)
    )


app.openapi = dynamic_io_schema_gen(ms=ModelService.load_from_disk(find_storage_root()))

if __name__ == '__main__':
    import uvicorn

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000)
