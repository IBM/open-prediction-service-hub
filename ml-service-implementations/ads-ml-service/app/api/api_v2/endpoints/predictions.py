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


import typing

import fastapi
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.core.cache as ops_cache
import app.core.uri as ops_rui
import app.crud as crud
import app.gen.schemas.ops_schemas as ops_schemas
import app.schemas.impl as impl

router = fastapi.APIRouter()


@router.post(
    path='/predictions',
    response_model=ops_schemas.PredictionResponse
)
def predict(
        pre_in: impl.PredictionImpl,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    endpoint_resource_list = list(filter(lambda link: link.rel == 'endpoint', pre_in.target))
    if len(endpoint_resource_list) != 1:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Predict accept one and only one endpoint')

    match = ops_rui.ADS_ML_SERVICE_RE.match(endpoint_resource_list[0].href)
    try:
        resource_path = match.group('resource_path')
        resource_id = int(match.group('resource_id'))
    except (AttributeError, ValueError):  # no match or failed conversion
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'Resource uri can not be parsed')

    if resource_path != '/endpoints':
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='/predictions only accept /endpoints as target')

    endpoint = crud.endpoint.get(db, id=resource_id)
    if endpoint is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='/endpoint resource not found')

    deserialized = ops_cache.cache.get_deserialized_model(db, endpoint_id=endpoint.id)
    if not deserialized:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Model file not found')

    return {
        'result': {
            'predict': deserialized.predict(
                {'instances': [[pair.value for pair in pre_in.parameters]]}
            )['predictions'][0]
        }
    }
