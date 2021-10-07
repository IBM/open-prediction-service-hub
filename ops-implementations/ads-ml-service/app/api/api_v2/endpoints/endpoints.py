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
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl

router = fastapi.APIRouter()


@router.get(
    path='/endpoints',
    response_model=ops_schemas.Endpoints,
    tags=['discover']
)
def get_endpoints(
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    return {
        'endpoints': [
            impl.EndpointImpl.from_database(endpoint)
            for endpoint in crud.endpoint.get_all(db)
        ]
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
    return impl.EndpointImpl.from_database(crud.endpoint.get(db, id=endpoint_id))


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
    crud.endpoint.update(db, db_obj=endpoint, obj_in=e_in)
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
    if not endpoint:
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    crud.endpoint.delete(db, id=endpoint_id)
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
