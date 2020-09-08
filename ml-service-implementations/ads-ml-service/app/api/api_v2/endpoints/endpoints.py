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
import joblib

import app.api.deps as deps
import app.crud as crud
import app.gen.schemas.ops_schemas as ops_schemas
import app.schemas as schemas
import app.schemas.impl as impl
import app.core.supported_lib as supported_lib

router = fastapi.APIRouter()


@router.get(
    path='/endpoints/{endpoint_id}',
    response_model=ops_schemas.Endpoint
)
def get_endpoints(
        endpoint_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    return impl.EndpointImpl.from_database(
        e=crud.endpoint.get(db, id=endpoint_id)
    )


@router.get(
    path='/endpoints',
    response_model=ops_schemas.Endpoints
)
def get_endpoints(
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    return {
        'endpoints': [
            impl.EndpointImpl.from_database(model)
            for model in crud.endpoint.get_all(db)
        ]
    }


@router.post(
    path='/endpoints',
    response_model=ops_schemas.Endpoint
)
def add_endpoint(
        model_id: int,
        m_in: ops_schemas.EndpointCreation,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    model = crud.model.get(db, id=model_id)
    if not model:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model not found')
    return impl.EndpointImpl.from_database(
        e=crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(name=m_in.name), model_id=model_id)
    )


@router.patch(
    path='/endpoints/{endpoint_id}',
    response_model=ops_schemas.Endpoint
)
def add_endpoint(
        endpoint_id: int,
        e_in: ops_schemas.EndpointUpdate,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if not endpoint:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Endpoint not found')
    return impl.EndpointImpl.from_database(
        e=crud.endpoint.update(
            db,
            db_obj=endpoint,
            obj_in=schemas.EndpointUpdate(name=e_in.name)
        )
    )


@router.delete(
    path='/endpoints/{endpoint_id}',
    status_code=status.HTTP_204_NO_CONTENT
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


@router.post(
    path='/endpoints/{endpoint_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def add_binary(
        endpoint_id: int,
        lib: supported_lib.MlLib = fastapi.Form(...),
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> responses.Response:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if not endpoint:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Endpoint not found')
    crud.binary_ml_model.create_with_endpoint(
        db,
        obj_in=schemas.BinaryMlModelCreate(
            model_b64=file.file.read(),
            library=lib
        ),
        endpoint_id=endpoint_id
    )
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
