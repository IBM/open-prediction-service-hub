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
import typing

import fastapi
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.core.uri as ops_uri
import app.gen.schemas.ops_schemas as ops_schemas
import app.runtime.cache as app_cache
import app.schemas.impl as impl

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)
ADDITIONAL_INFO_NAME = 'additional_info'


@router.post(
    path='/predictions',
    response_model=ops_schemas.PredictionResponse
)
async def predict(
        pre_in: impl.PredictionImpl,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    LOGGER.info('Prediction input: %s', pre_in)

    endpoint_resources = (link for link in pre_in.target if link.rel == 'endpoint')
    endpoint_resource = next(endpoint_resources, None)
    if endpoint_resource is None or next(endpoint_resources, None) is not None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Predict accept one and only one endpoint')

    match = ops_uri.ADS_ML_SERVICE_RE.match(endpoint_resource.href)
    try:
        resource_path = match.group('resource_path')
        resource_id = int(match.group('resource_id'))
    except (AttributeError, ValueError):  # no match or failed conversion
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'Resource uri can not be parsed')

    if resource_path != '/endpoints':
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='/predictions only accept /endpoints as target')

    deserialized = app_cache.cache.get_deserialized_model(db, endpoint_id=resource_id)
    if not deserialized:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Resource not found')

    params = [param for param in pre_in.parameters]
    prediction_output = deserialized.predict(params)

    model = crud.model_config.get(db, id=endpoint.id)  # The model exists since the endpoint exists
    metadata = model.configuration.get('metadata')
    additional_metadata = {} if \
        not metadata or not metadata.get(ADDITIONAL_INFO_NAME) else \
        metadata[ADDITIONAL_INFO_NAME]

    LOGGER.info('Prediction output: %s', prediction_output)
    return prediction_output
