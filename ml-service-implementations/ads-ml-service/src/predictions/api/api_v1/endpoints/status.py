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

from fastapi import APIRouter, Depends

from ...deps import get_ml_service
from ....core.open_prediction_service import OpenPredictionService
from ....schemas.prediction import ServerStatus

router = APIRouter()


@router.get(
    tags=['Admin'],
    path='/status',
    response_model=ServerStatus
)
def get_server_status(mls: OpenPredictionService = Depends(get_ml_service)) -> ServerStatus:
    return ServerStatus(model_count=mls.count_models())
