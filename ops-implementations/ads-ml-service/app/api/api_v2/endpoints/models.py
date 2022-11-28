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
import app.gen.schemas.ops_schemas as ops_schemas
import app.runtime.model_upload as app_model_upload
import app.runtime.inspection as app_runtime_inspection
import app.schemas as schemas
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl
import app.core.configuration as app_conf

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    path='/models',
    response_model=impl.ModelsImpl,
    tags=['discover']
)
def get_models(
        db: saorm.Session = fastapi.Depends(deps.get_db),
        total_count: typing.Optional[bool] = False,
        offset: typing.Optional[int] = 0,
        limit: typing.Optional[int] = 100
) -> typing.Dict[typing.Text, typing.Any]:
    if not (0 < limit <= app_conf.get_config().MAX_PAGE_SIZE and offset >= 0):
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Requested offset/limit is not valid')
    return {
        'models': [
            impl.ModelImpl.from_database(model)
            for model in crud.model.get_multi(db, skip=offset, limit=limit)
        ],
        'total_count': 0 if not total_count else crud.model.count(db)
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
    model = crud.model.get(db, id=model_id)
    if model is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')
    return impl.ModelImpl.from_database(
        db_obj=model
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
    model = crud.model.get(db, id=model_id)
    if model is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')
    update_data = m_in.dict(exclude_unset=True)
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
    if model is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')
    crud.model.delete(db, id=model_id)
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    path='/models/{model_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=ops_schemas.Endpoint,
    tags=['manage']
)
async def add_binary(
        model_id: int,
        input_data_structure: app_binary_config.ModelInput = fastapi.Form(app_binary_config.ModelInput.AUTO),
        output_data_structure: app_binary_config.ModelOutput = fastapi.Form(app_binary_config.ModelOutput.AUTO),
        format_: app_binary_config.ModelWrapper = fastapi.Form(app_binary_config.ModelWrapper.PICKLE, alias='format'),
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> ops_schemas.Endpoint:
    model = crud.model.get(db, id=model_id)
    if model is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')

    model_binary = await file.read()

    if not app_model_upload.is_compatible(model_binary, format_):
        raise fastapi.HTTPException(status_code=422, detail='Can not deserialize model binary')

    m = app_model_upload.store_model(
        db,
        model_binary,
        input_data_structure=input_data_structure,
        output_data_structure=output_data_structure,
        format_=format_,
        model_id=model_id
    )
    return impl.EndpointImpl.from_database(crud.endpoint.get(db, id=m))


@router.get(
    path='/models/{model_id}/metadata',
    response_model=typing.Union[ops_schemas.AdditionalPickleModelInfo, ops_schemas.AdditionalPMMLModelInfo],
    tags=['discover']
)
def get_model_metadata(
        model_id: int,
        db: saorm.Session = fastapi.Depends(deps.get_db)):
    LOGGER.info('Retrieving model metadata for id: %s', model_id)
    model = crud.binary_ml_model.get(db=db, id=model_id)

    if model is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Model with id {model_id} is not found')

    if model.format == app_binary_config.ModelWrapper.PICKLE:
        return ops_schemas.AdditionalPickleModelInfo(
            modelType='pickle', pickleProtoVersion=str(app_runtime_inspection.inspect_pickle_version(model.model_b64)))
    elif model.format == app_binary_config.ModelWrapper.PMML:
        return ops_schemas.AdditionalPMMLModelInfo(
            modelType='pmml', modelSubType=str(app_runtime_inspection.inspect_pmml_subtype(model.model_b64)))
    else:
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Format {model.format} is not supported for metadata')
