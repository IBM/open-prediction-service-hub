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
import fastapi.responses as responses
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.crud as crud
import app.gen.schemas.ops_schemas as ops_schemas
import app.schemas as schemas
import app.schemas.impl as impl
import app.core.configuration as app_conf

router = fastapi.APIRouter()


@router.get(
    path='/endpoints',
    response_model=ops_schemas.Endpoints,
    tags=['discover']
)
def get_endpoints(
        db: saorm.Session = fastapi.Depends(deps.get_db),
        model_id: typing.Optional[int] = -1,
        total_count: typing.Optional[bool] = False,
        offset: typing.Optional[int] = 0,
        limit: typing.Optional[int] = 100
) -> typing.Dict[typing.Text, typing.Any]:
    if not (0 < limit <= app_conf.get_config().MAX_PAGE_SIZE and offset >= 0):
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Requested offset/limit is not valid')
    if model_id != -1:
        model = crud.model.get(db, id=model_id)
        if model is None:
            raise fastapi.HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')
        return {
            'endpoints': [impl.EndpointImpl.from_database(model.endpoint)],
            'total_count': 0 if not total_count else 1
        }
    return {
        'endpoints': [
            impl.EndpointImpl.from_database(endpoint)
            for endpoint in crud.endpoint.get_multi(db, skip=offset, limit=limit)
        ],
        'total_count': 0 if not total_count else crud.endpoint.count(db)
    }


@router.get(
    path='/endpoints/{endpoint_id}',
    response_model=ops_schemas.Endpoint,
    tags=['discover']
)
def get_endpoint(
        endpoint_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if endpoint is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Endpoint with id {endpoint_id} is not found')
    return impl.EndpointImpl.from_database(endpoint)


@router.patch(
    path='/endpoints/{endpoint_id}',
    response_model=ops_schemas.Endpoint,
    tags=['manage']
)
def patch_endpoint(
        endpoint_id: int,
        e_in: ops_schemas.EndpointUpdate,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if endpoint is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Endpoint with id {endpoint_id} is not found')
    endpoint_in = e_in.dict(exclude_unset=True)
    if endpoint_in.get('metadata'):
        endpoint_in['metadata_'] = endpoint_in.pop('metadata')
    crud.endpoint.update(db, db_obj=endpoint, obj_in=schemas.EndpointUpdate(**endpoint_in))
    return impl.EndpointImpl.from_database(endpoint)


@router.delete(
    path='/endpoints/{endpoint_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['manage']
)
def delete_endpoint(
        endpoint_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> responses.Response:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if endpoint is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Endpoint with id {endpoint_id} is not found')
    crud.endpoint.delete(db, id=endpoint_id)
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
