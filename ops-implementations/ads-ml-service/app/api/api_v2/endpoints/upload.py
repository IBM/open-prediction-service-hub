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
import fastapi.encoders as encoders
import sqlalchemy.orm as saorm
import starlette.status as status

import app.api.deps as deps
import app.crud as crud
import app.runtime.signature_inspection as app_signature_inspection
import app.runtime.wrapper as app_runtime_wrapper
import app.schemas as schemas
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
        file: fastapi.UploadFile = fastapi.File(...),
        db: saorm.Session = fastapi.Depends(deps.get_db)
) -> typing.Dict[typing.Text, typing.Any]:
    model_name, model_extension = os.path.splitext(file.filename)[0], os.path.splitext(file.filename)[1]
    model_binary = await file.read()

    if model_extension.lower() not in ('.pmml',):
        raise fastapi.HTTPException(status_code=422, detail="File extension not supported")

    # test pmml compatibility
    try:
        app_runtime_wrapper.ModelInvocationExecutor(
            model=model_binary,
            input_type=app_binary_config.ModelInput.DATAFRAME,
            output_type=app_binary_config.ModelOutput.DATAFRAME,
            binary_format=app_binary_config.ModelWrapper.PMML,
            info={}
        )
    except Exception:
        raise fastapi.HTTPException(status_code=422, detail="Can not deserialize model binary")

    input_schema = app_signature_inspection.inspect_pmml_input(model_binary)
    output_schema = app_signature_inspection.inspect_pmml_output(model_binary)

    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db,
        obj_in=schemas.ModelConfigCreate(
            configuration=encoders.jsonable_encoder(
                obj=impl.ModelCreateImpl(
                    name=model_name,
                    input_schema=[
                        impl.FeatureImpl(
                            name=k,
                            order=i,
                            type=input_schema[k]
                        ) for i, k in enumerate(input_schema.keys())
                    ],
                    output_schema={
                        k: {
                            'type': v
                        }
                        for k, v in output_schema.items()
                    }
                )
            )
        ),
        model_id=model.id
    )
    LOGGER.info('Created model \'%s\'', model.id)

    crud.endpoint.create_with_model_and_binary(
        db,
        model_id=model.id,
        ec=schemas.EndpointCreate(name=model_name),
        bc=schemas.BinaryMlModelCreate(
            model_b64=model_binary,
            input_data_structure=app_binary_config.ModelInput.DATAFRAME,
            output_data_structure=app_binary_config.ModelOutput.DATAFRAME,
            format=app_binary_config.ModelWrapper.PMML)
    )

    refreshed_model = crud.model.get(db, id=model.id)

    return impl.ModelImpl.from_database(
        db_obj=refreshed_model
    )
