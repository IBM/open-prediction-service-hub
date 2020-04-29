#!/usr/bin/env python3

import logging
from logging import Logger
from operator import itemgetter
from typing import Text, List

import numpy as np
from dynamic_hosting.core.configuration import ServerConfiguration
from dynamic_hosting.core.model import Model, MLSchema
from dynamic_hosting.core.model_service import ModelService
from dynamic_hosting.core.util import to_dataframe_compatible
from dynamic_hosting.openapi.request import RequestBody
from dynamic_hosting.openapi.response import FeatProbaPair, ServerStatus, Prediction
from fastapi import FastAPI, File

from fastapi_versioning import VersionedFastAPI, version

app: FastAPI = FastAPI(
    version='0.0.0-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model'
)

VER: int = 1


@app.get(
    tags=['Admin'],
    path='/status',
    response_model=ServerStatus
)
@version(major=VER)
def get_server_status() -> ServerStatus:
    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)
    return ServerStatus(model_count=len(ms.ml_models))


@app.get(
    tags=['Admin'],
    path='/models',
    response_model=List[MLSchema]
)
@version(major=VER)
def get_models() -> List[MLSchema]:
    """Returns the list of ML models."""
    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)
    return [
        model.get_meta_model() for model in ms.ml_models
    ]


@app.post(
    tags=['Admin'],
    path='/models',
    responses={
        200: {
            'description': 'Model has been uploaded successfully',
        }
    }
)
@version(major=VER)
def add_model(*, file: bytes = File(...)) -> None:
    ModelService.load_from_disk(ServerConfiguration().model_storage).add_archive(file)


@app.delete(
    tags=['Admin'],
    path='/models'
)
@version(major=VER)
def remove_model(*, model_name: Text, model_version: Text = None) -> None:
    ModelService.load_from_disk(ServerConfiguration().model_storage).remove_model(model_name=model_name,
                                                                                  model_version=model_version)


@app.post(
    tags=['ML'],
    path='/invocations',
    response_model=Prediction
)
@version(major=VER)
def predict(
        *,
        ml_req: RequestBody
) -> Prediction:
    logger: Logger = logging.getLogger(__name__)

    logger.debug('Received request: {r}'.format(r=ml_req))

    ms: ModelService = ModelService.load_from_disk(ServerConfiguration().model_storage)

    model: Model = ms.model_map()[ml_req.get_model_name()][ml_req.get_model_version()]

    res_matrix: np.ndarray = ms.invoke(
        model_name=ml_req.get_model_name(),
        model_version=ml_req.get_model_version(),
        data=to_dataframe_compatible(ml_req.get_data())
    )

    res = res_matrix[0]  # one input -> one output

    if model.method_name == 'predict_proba' and isinstance(res, np.ndarray) and model.has_attr('classes_'):
        feature_names: List[Text] = model.get_attr('classes_')

        return Prediction(
            prediction=feature_names[max(enumerate(res), key=itemgetter(1))[0]],
            probabilities=[
                FeatProbaPair(name=feature_names[i], proba=res[i])
                for i in range(len(feature_names))
            ]
        )
    else:
        return Prediction(prediction=res, probabilities=None)


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
