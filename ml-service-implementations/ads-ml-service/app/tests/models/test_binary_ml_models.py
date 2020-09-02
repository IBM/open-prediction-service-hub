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

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.models as models


def test_working_config(db: Session, classification_predictor):
    binary_model = models.BinaryMLModel(model_b64=pickle.dumps(classification_predictor), library=models.MlLib.SKLearn)
    db.add(binary_model)
    db.commit()
    db.refresh(binary_model)

    assert binary_model.model_b64
    assert binary_model.library == models.MlLib.SKLearn


def test_add_binary_without_lib(db: Session, classification_predictor):
    binary_model = models.BinaryMLModel(model_b64=pickle.dumps(classification_predictor))
    db.add(binary_model)

    with pytest.raises(IntegrityError):
        db.commit()
        db.refresh(binary_model)
