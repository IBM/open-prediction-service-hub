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
import os
import typing

import fastapi
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.crud as crud
import app.runtime.model_upload as app_model_upload
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl
import app.runtime.inspection as app_inspection

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post(
    path='/upload',
    status_code=status.HTTP_201_CREATED,
    response_model=impl.ModelImpl,
    tags=['manage']
)
async def upload(
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[str, typing.Any]:
    LOGGER.info('Receiving file %s', file.filename)
    file_name, file_extension = os.path.splitext(file.filename)
    model_binary = await file.read()

    if file_extension.lower() not in app_model_upload.SUPPORTED_FORMATS:
        LOGGER.warning(
            'File extension is not supported: %s, expected: %s', file.filename, app_model_upload.SUPPORTED_FORMATS)
        raise fastapi.HTTPException(
            status_code=422,
            detail='File extension is not supported: %s, expected: %s' % (
                file.filename, app_model_upload.SUPPORTED_FORMATS)
        )

    formatted_extension = file_extension.upper()[1:]
    try:
        model_format = app_binary_config.ModelWrapper[formatted_extension]
    except KeyError:
        raise fastapi.HTTPException(status_code=422, detail=f'Model extension {formatted_extension} not supported')

    if not app_model_upload.is_compatible(model_binary, model_format):
        raise fastapi.HTTPException(status_code=422, detail=f'Model can not be loaded. Model type: {model_format}')

    if model_format is app_binary_config.ModelWrapper.PMML:
        inspected_name = app_inspection.inspect_pmml_model_name(model_binary)
        model_name = inspected_name if inspected_name is not None else file_name
    else:
        model_name = file_name

    m = app_model_upload.store_model(
        db,
        model_binary,
        input_data_structure=app_binary_config.ModelInput.DATAFRAME,
        output_data_structure=app_binary_config.ModelOutput.DATAFRAME,
        format_=app_binary_config.ModelWrapper.PMML,
        name=model_name
    )

    return impl.ModelImpl.from_database(
        db_obj=crud.model.get(db, id=m)
    )
