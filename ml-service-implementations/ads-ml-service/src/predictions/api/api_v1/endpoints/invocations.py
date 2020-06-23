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
from typing import List, Text

import numpy as np
from fastapi import APIRouter, Depends

from ...deps import get_ml_service
from ....schemas.model import Model
from ....core.util import to_dataframe_compatible
from ....core.open_predict_service import PredictionService
from ....schemas.request import RequestBody
from ....schemas.prediction import Probability, Prediction

router = APIRouter()


@router.post(
    tags=['ML'],
    path='/invocations',
    response_model=Prediction
)
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

    if model.info.method_name == 'predict_proba' and isinstance(res, np.ndarray):
        feature_names: List[Text] = [
            class_name for class_name in
            sorted((v for i, v in model.info.metadata.class_names.items()), key=itemgetter(0))
        ] if model.info.metadata.class_names is not None else list(range(len(res)))

        return Prediction(
            prediction=feature_names[max(enumerate(res), key=itemgetter(1))[0]],
            probabilities=[
                Probability(class_name=feature_names[i], class_index=i, value=res[i])
                for i in range(len(feature_names))
            ]
        )
    else:
        return Prediction(prediction=res, probabilities=None)
