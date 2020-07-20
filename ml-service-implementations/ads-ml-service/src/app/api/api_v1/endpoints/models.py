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
from typing import List, Dict, Text

from fastapi import APIRouter, Depends, File

from ...deps import get_ml_service
from ....core.open_prediction_service import OpenPredictionService
from ....schemas.model import MLSchema

router = APIRouter()


@router.get(
    path='/models',
    response_model=List[MLSchema]
)
def get_models(mls: OpenPredictionService = Depends(get_ml_service)) -> List[MLSchema]:
    """Returns the list of ML models."""
    return mls.get_model_configs()


@router.post(
    path='/models',
    responses={
        200: {
            'description': 'Model has been uploaded successfully',
        }
    }
)
def add_model(*, file: bytes = File(...), mls: OpenPredictionService = Depends(get_ml_service)) -> None:
    mls.add_archive(file)


@router.delete(
    tags=['Admin'],
    path='/models'
)
def remove_model(*, model_name: Text, model_version: Text = None, mls: OpenPredictionService = Depends(get_ml_service)) -> None:
    mls.remove_model(model_name=model_name, model_version=model_version)