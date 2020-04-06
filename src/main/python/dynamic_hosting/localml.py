#!/usr/bin/env python3

import logging
import sys
from logging import Logger
from operator import itemgetter
from typing import Callable, Text, Mapping, Type, Tuple, Any, Union, List

import numpy as np
from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.core.model import Model, MetaMLModel
from dynamic_hosting.openapi.request import RequestBody
from dynamic_hosting.openapi.response import BaseResponseBody, PredictResponseBody, PredictProbaResponseBody, \
    FeatProbaPair
from dynamic_hosting.core.util import storage_root, load_direct_request_schema, replace_any_of, \
    get_real_request_class, replace_any_of_in_response
from fastapi import FastAPI, File
from fastapi.exceptions import HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.utils import get_model_definitions
from pandas import DataFrame
from pydantic import BaseModel, ValidationError

app = FastAPI(
    version='0.0.0-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model',
    docs_url='/'
)


@app.get(tags=['Admin'], path='/isAlive', response_model=Mapping)
def heart_beat() -> Mapping:
    return {'status': 'good'}


@app.get(tags=['Admin'], path='/models', response_model=List[MetaMLModel])
def get_models() -> List[MetaMLModel]:
    """Returns the list of ML models."""
    ms: ModelService = ModelService.load_from_disk(storage_root())
    return [
        model.get_meta_model() for model in ms.ml_models
    ]


@app.post(
    tags=['Admin'],
    path='/archives',
    responses={
        200: {
            'description': 'Model has been uploaded successfully',
        }
    }
)
def add_model(*, file: bytes = File(...)) -> None:
    ModelService.load_from_disk(storage_root()).add_archive(file)


@app.delete(tags=['Admin'], path='/models')
def remove_model(*, model_name: Text, model_version: Text = None) -> None:
    ModelService.load_from_disk(storage_root()).remove_model(model_name=model_name, model_version=model_version)


@app.post(tags=['ML'], path='/invocation',
          response_model=Union[PredictProbaResponseBody, PredictResponseBody, BaseResponseBody])
def predict(
        *,
        ml_req: RequestBody
) -> BaseResponseBody:
    logger: Logger = logging.getLogger(__name__)

    logger.info('Received request: {r}'.format(r=ml_req))

    ms: ModelService = ModelService.load_from_disk(storage_root())

    model_name: Text = ml_req.get_model_name()
    model_version: Text = ml_req.get_model_version()
    model: Model = ms.model_map()[ml_req.get_model_name()][ml_req.get_model_version()]

    res_data: Any = ms.invoke(
        model_name=model_name,
        model_version=model_version,
        data=model.to_dataframe_compatible(ml_req.get_data())
    )

    # We suppose the most common output of ml model is ndarray
    try:
        if model.method_name == 'predict':
            if isinstance(res_data, np.ndarray) and len(res_data) == 1:
                return PredictResponseBody(
                    raw_output=DataFrame(res_data).to_dict(),
                    predict_output=str(res_data[0])
                )
            else:
                return BaseResponseBody(
                    raw_output=DataFrame(res_data).to_dict()
                )
        elif model.method_name == 'predict_proba':
            res_line = res_data[0]  # We have only one instance
            feature_names: List[Text] = model.get_model_attr('classes_')

            assert np.isclose(sum(res_line), 1, rtol=1e-08, atol=1e-08, equal_nan=False)  # The sum needs to be 1
            assert len(feature_names) == len(res_line)

            x = PredictProbaResponseBody(
                raw_output=DataFrame(res_line).to_dict(),
                predict_output=feature_names[max(enumerate(res_line), key=itemgetter(1))[0]],
                probabilities=[
                    FeatProbaPair(name=feature_names[i], proba=res_line[i])
                    for i in range(len(feature_names))
                ]
            )
            return x
    except ValidationError:
        return BaseResponseBody(
            raw_output=str(res_data)
        )


if __name__ == '__main__':
    import uvicorn

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
