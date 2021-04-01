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

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post(
    path='/upload',
    status_code=status.HTTP_201_CREATED,
    response_model=impl.ModelImpl,
    tags=['manage']
)
async def upload(
        format_: str = fastapi.Form(..., alias='format'),
        name: typing.Optional[str] = fastapi.Form(None),
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    file_name = os.path.splitext(file.filename)[0]
    model_extension = os.path.splitext(file.filename)[1]

    if model_extension.lower() not in ('.pmml',):
        LOGGER.warning('File extension is not supported: %s', file.filename)
    if format_.lower() not in ('pmml',):
        raise fastapi.HTTPException(status_code=422, detail="File extension not supported")

    m = await app_model_upload.upload_model(
        db,
        file,
        input_data_structure=app_binary_config.ModelInput.DATAFRAME,
        output_data_structure=app_binary_config.ModelOutput.DATAFRAME,
        format_=app_binary_config.ModelWrapper.PMML,
        name=name if name is not None else file_name
    )

    return impl.ModelImpl.from_database(
        db_obj=crud.model.get(db, id=m)
    )
