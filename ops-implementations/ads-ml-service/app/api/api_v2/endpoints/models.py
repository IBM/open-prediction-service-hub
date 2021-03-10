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
import fastapi.encoders as encoders
import fastapi.responses as responses
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.crud as crud
import app.schemas as schemas
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl
import app.gen.schemas.ops_schemas as ops_schemas
import app.runtime.wrapper as app_runtime_wrapper

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    path='/models',
    response_model=impl.ModelsImpl,
    tags=['discover']
)
def get_models(
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    return {
        'models': [
            impl.ModelImpl.from_database(model)
            for model in crud.model.get_all(db)
        ]
    }


@router.get(
    path='/models/{model_id}',
    response_model=impl.ModelImpl,
    tags=['discover']
)
def get_model(
        model_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    return impl.ModelImpl.from_database(
        db_obj=crud.model.get(db, id=model_id)
    )


@router.post(
    path='/models',
    status_code=status.HTTP_201_CREATED,
    response_model=impl.ModelImpl,
    tags=['manage']
)
def add_model(
        m_in: impl.ModelCreateImpl,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db,
        obj_in=schemas.ModelConfigCreate(
            configuration=encoders.jsonable_encoder(obj=m_in)
        ),
        model_id=model.id
    )
    LOGGER.info('Created model \'%s\'', model.id)
    return impl.ModelImpl.from_database(
        db_obj=model
    )


@router.patch(
    path='/models/{model_id}',
    response_model=impl.ModelImpl,
    tags=['manage']
)
def patch_model(
        model_id: int,
        m_in: impl.ModelUpdateImpl,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    update_data = m_in.dict(exclude_unset=True)
    model = crud.model.get(db, id=model_id)
    new_config = {
        field: update_data[field] if field in update_data else model.config.configuration[field]
        for field in model.config.configuration
    }
    crud.model_config.update(
        db,
        db_obj=model.config,
        obj_in=schemas.ModelConfigUpdate(configuration=new_config)
    )
    return impl.ModelImpl.from_database(
        db_obj=model
    )


@router.delete(
    path='/models/{model_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['manage']
)
def delete_model(
        model_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> responses.Response:
    LOGGER.info('Deleting model %s', model_id)
    model = crud.model.get(db, id=model_id)
    if not model:
        LOGGER.info('Model %s not found', model_id)
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    crud.model.delete(db, id=model_id)
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    path='/models/{model_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=ops_schemas.Endpoint,
    tags=['manage']
)
def add_binary(
        model_id: int,
        input_data_structure: app_binary_config.ModelInput = fastapi.Form(app_binary_config.ModelInput.AUTO),
        output_data_structure: app_binary_config.ModelOutput = fastapi.Form(app_binary_config.ModelOutput.AUTO),
        format: app_binary_config.ModelWrapper = fastapi.Form(app_binary_config.ModelWrapper.PICKLE),
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> ops_schemas.Endpoint:
    LOGGER.info('Adding binary for model %s', model_id)
    model_config = crud.model_config.get(db, id=model_id)
    model = file.file.read()
    if not model_config:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model not found')

    # test model compatibility
    try:
        app_runtime_wrapper.ModelInvocationExecutor(
            model=model,
            input_type=input_data_structure,
            output_type=output_data_structure,
            binary_format=format,
            info={}
        )
    except:
        raise fastapi.HTTPException(status_code=422, detail="Can not deserialize model binary")

    endpoint = crud.endpoint.get(db, id=model_id)
    if not endpoint:
        LOGGER.info('Endpoint not exist, creating')
        # Creation
        endpoint_db_obj = crud.endpoint.create_with_model_and_binary(
            db,
            model_id=model_id,
            ec=schemas.EndpointCreate(name=model_config.configuration['name']),
            bc=schemas.BinaryMlModelCreate(
                model_b64=file.file.read(),
                input_data_structure=input_data_structure,
                output_data_structure=output_data_structure,
                format=format))
        return impl.EndpointImpl.from_database(endpoint_db_obj)
    else:
        LOGGER.info('Endpoint exist, updating')
        endpoint_updated = crud.endpoint.update_binary(
            db,
            e=endpoint,
            bu=schemas.BinaryMlModelUpdate(
                model_b64=file.file.read(),
                input_data_structure=input_data_structure,
                output_data_structure=output_data_structure,
                format=format
            )
        )
        return impl.EndpointImpl.from_database(endpoint_updated)
