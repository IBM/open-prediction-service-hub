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


import logging
from logging import Logger
from operator import itemgetter
from typing import Text, List, Optional

import numpy as np
from dynamic_hosting.core.configuration import ServerConfiguration
from dynamic_hosting.core.model import Model, MLSchema
from dynamic_hosting.open_predict_service import PredictionService
from dynamic_hosting.core.util import to_dataframe_compatible
from dynamic_hosting.db import models
from dynamic_hosting.openapi.request import RequestBody
from dynamic_hosting.openapi.response import Probability, ServerStatus, Prediction
from fastapi import FastAPI, File, Depends

from fastapi_versioning import VersionedFastAPI, version
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

app: FastAPI = FastAPI(
    version='0.0.0-SNAPSHOT',
    title='Local ml provider',
    description='A simple environment to test machine learning model'
)

VER: int = 1
DATABASE_NAME: Text = 'EML.db'


# Dependency
def get_ml_service() -> PredictionService:
    logger: Logger = logging.getLogger(__name__)
    engine: Engine = create_engine(
        f'sqlite:///{ServerConfiguration().model_storage.joinpath(DATABASE_NAME)}',
        connect_args={"check_same_thread": False}
    )
    models.Base.metadata.create_all(bind=engine)
    sm_instance: sessionmaker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = None
    try:
        db = sm_instance()
        mls: PredictionService = PredictionService(db=db)
        yield mls
    finally:
        db.close()


@app.get(
    tags=['Admin'],
    path='/status',
    response_model=ServerStatus
)
@version(major=VER)
def get_server_status(mls: PredictionService = Depends(get_ml_service)) -> ServerStatus:
    return ServerStatus(model_count=len(mls.get_models()))


@app.get(
    tags=['Admin'],
    path='/models',
    response_model=List[MLSchema]
)
@version(major=VER)
def get_models(mls: PredictionService = Depends(get_ml_service)) -> List[MLSchema]:
    """Returns the list of ML models."""
    return [
        model.get_meta_model() for model in mls.get_models()
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
def add_model(*, file: bytes = File(...), mls: PredictionService = Depends(get_ml_service)) -> None:
    mls.add_archive(file)


@app.delete(
    tags=['Admin'],
    path='/models'
)
@version(major=VER)
def remove_model(*, model_name: Text, model_version: Text = None, mls: PredictionService = Depends(get_ml_service)) -> None:
    mls.remove_model(model_name=model_name, model_version=model_version)


@app.post(
    tags=['ML'],
    path='/invocations',
    response_model=Prediction
)
@version(major=VER)
def predict(
        *,
        ml_req: RequestBody,
        mls: PredictionService = Depends(get_ml_service)
) -> Prediction:
    logger: Logger = logging.getLogger(__name__)

    logger.debug('Received request: {r}'.format(r=ml_req))

    model: Model = mls.get_model(model_name=ml_req.get_model_name(), model_version=ml_req.get_model_version())

    res_matrix: np.ndarray = mls.invoke(
        model_name=ml_req.get_model_name(),
        model_version=ml_req.get_model_version(),
        data=to_dataframe_compatible(ml_req.get_data())
    )

    res: np.ndaary = res_matrix[0]  # one input -> one output

    if model.method_name == 'predict_proba' and isinstance(res, np.ndarray):
        feature_names: List[Text] = [
            class_name for class_name in sorted((v for i, v in model.metadata.class_names.items()), key=itemgetter(0))
        ] if model.metadata.class_names is not None else list(range(len(res)))

        return Prediction(
            prediction=feature_names[max(enumerate(res), key=itemgetter(1))[0]],
            probabilities=[
                Probability(class_name=feature_names[i], class_index=i, value=res[i])
                for i in range(len(feature_names))
            ]
        )
    else:
        return Prediction(prediction=res, probabilities=None)


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
