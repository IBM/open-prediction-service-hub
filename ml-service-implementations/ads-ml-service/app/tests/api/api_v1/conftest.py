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


import pickle
from typing import Any, Dict

import pytest

from .... import crud
from ....schemas.binary_ml_model import BinaryMLModelCreate
from ....schemas.model import ModelCreate
from ....schemas.model_config import ModelConfigCreate
from ....models.model import Model


def model_prepare(binary: Any, conf: Dict) -> ModelCreate:
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(binary))
    config_in = ModelConfigCreate(**conf)

    return ModelCreate(
        name=conf['name'],
        version=conf['version'],
        binary=binary_in,
        config=config_in
    )


@pytest.fixture
def classification_archive(client, db, classification_predictor, classification_config) -> Model:
    model_in = model_prepare(classification_predictor, classification_config)
    return crud.crud_model.model.create(db, obj_in=model_in)


@pytest.fixture
def classification_with_proba_archive(client, db, classification_with_prob_predictor, classification_prob_config) -> Model:
    model_in = model_prepare(classification_with_prob_predictor, classification_prob_config)
    return crud.crud_model.model.create(db, obj_in=model_in)


@pytest.fixture
def regression_archive(client, db, regression_predictor, regression_config) -> Model:
    model_in = model_prepare(regression_predictor, regression_config)
    return crud.crud_model.model.create(db, obj_in=model_in)
