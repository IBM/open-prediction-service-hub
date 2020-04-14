#!/usr/bin/env python3

import logging
from logging import Logger
from operator import itemgetter
from typing import Text, Any, List

import numpy as np
from dynamic_hosting.core.configuration import ServerConfiguration
from dynamic_hosting.core.model import Model, MLSchema
from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.openapi.request import RequestBody
from dynamic_hosting.openapi.response import BaseResponseBody, PredictProbaResponse, \
    FeatProbaPair, ClassificationResponse, RegressionResponse, ServerStatus
from fastapi import FastAPI, File
from pandas import DataFrame
from pydantic import ValidationError

app = FastAPI(
    version='0.0.0-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model',
    docs_url='/'
)


def _predict(ml_req: RequestBody, ms: ModelService) -> Any:

    model: Model = ms.model_map()[ml_req.get_model_name()][ml_req.get_model_version()]

    res_data: Any = ms.invoke(
        model_name=ml_req.get_model_name(),
        model_version=ml_req.get_model_version(),
        data=model.to_dataframe_compatible(ml_req.get_data())
    )

    return res_data


@app.get(tags=['Admin'], path='/status', response_model=ServerStatus)
def get_server_status() -> ServerStatus:
    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)
    return ServerStatus(count=len(ms.ml_models))


@app.get(tags=['Admin'], path='/models', response_model=List[MLSchema])
def get_models() -> List[MLSchema]:
    """Returns the list of ML models."""
    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)
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
    ModelService.load_from_disk(ServerConfiguration().model_storage).add_archive(file)


@app.delete(tags=['Admin'], path='/models')
def remove_model(*, model_name: Text, model_version: Text = None) -> None:
    ModelService.load_from_disk(ServerConfiguration().model_storage).remove_model(model_name=model_name, model_version=model_version)


@app.post(tags=['ML'], path='/classification',
          response_model=ClassificationResponse)
def classification(
        *,
        ml_req: RequestBody
) -> ClassificationResponse:
    logger: Logger = logging.getLogger(__name__)

    logger.info('Received request: {r}'.format(r=ml_req))

    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)

    res_data: Any = _predict(ml_req=ml_req, ms=ms)

    # We suppose the most common output of ml model is ndarray
    if isinstance(res_data, np.ndarray) and len(res_data) == 1:
        return ClassificationResponse(
            classification_output=str(res_data[0])
        )
    else:
        raise ValueError('Model output can not be serialized, Raw output: {raw}'.format(raw=BaseResponseBody(
                    raw_output=DataFrame(res_data).to_dict()
                )))


@app.post(tags=['ML'], path='/regression',
          response_model=RegressionResponse)
def regression(
        *,
        ml_req: RequestBody
) -> RegressionResponse:
    logger: Logger = logging.getLogger(__name__)

    logger.info('Received request: {r}'.format(r=ml_req))

    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)

    res_data: Any = _predict(ml_req=ml_req, ms=ms)

    # We suppose the most common output of ml model is ndarray
    if isinstance(res_data, np.ndarray) and len(res_data) == 1:
        return RegressionResponse(
            regression_output=float(res_data[0])
        )
    else:
        raise ValueError('Model output can not be serialized, Raw output: {raw}'.format(raw=BaseResponseBody(
            raw_output=DataFrame(res_data).to_dict()
        )))


@app.post(tags=['ML'], path='/predict_proba',
          response_model=PredictProbaResponse)
def predict_proba(
        *,
        ml_req: RequestBody
) -> PredictProbaResponse:
    logger: Logger = logging.getLogger(__name__)

    logger.info('Received request: {r}'.format(r=ml_req))

    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)

    model: Model = ms.model_map()[ml_req.get_model_name()][ml_req.get_model_version()]

    res_data: Any = _predict(ml_req=ml_req, ms=ms)

    # We suppose the most common output of ml model is ndarray
    try:
        if model.method_name == 'predict_proba':
            res_line = res_data[0]  # We have only one instance
            feature_names: List[Text] = model.get_model_attr('classes_')

            assert len(feature_names) == len(res_line)

            return PredictProbaResponse(
                predict_output=feature_names[max(enumerate(res_line), key=itemgetter(1))[0]],
                probabilities=[
                    FeatProbaPair(name=feature_names[i], proba=res_line[i])
                    for i in range(len(feature_names))
                ]
            )
    except ValidationError:
        raise ValueError('Model output can not be serialized, Raw output: {raw}'.format(raw=BaseResponseBody(
            raw_output=DataFrame(res_data).to_dict()
        )))
