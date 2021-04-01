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

import app.crud as crud
import app.runtime.signature_inspection as app_signature_inspection
import app.runtime.wrapper as app_runtime_wrapper
import app.schemas as schemas
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)


async def upload_model(
        db: saorm.Session,
        file: fastapi.UploadFile,
        input_data_structure: app_binary_config.ModelInput = None,
        output_data_structure: app_binary_config.ModelOutput = None,
        format_: app_binary_config.ModelWrapper = None,
        model_id: typing.Optional[int] = None
) -> int:
    file_name = os.path.splitext(file.filename)[0]
    model_binary = await file.read()

    # test model_binary compatibility
    try:
        app_runtime_wrapper.ModelInvocationExecutor(
            model=model_binary,
            input_type=input_data_structure,
            output_type=output_data_structure,
            binary_format=format_
        )
    except Exception:
        raise fastapi.HTTPException(status_code=422, detail='Can not deserialize model binary')

    if model_id is None:
        LOGGER.info('Adding binary directly')

        input_schema = app_signature_inspection.inspect_pmml_input(model_binary)
        output_schema = app_signature_inspection.inspect_pmml_output(model_binary)

        model = crud.model.create(db, obj_in=schemas.ModelCreate())
        crud.model_config.create_with_model(
            db,
            obj_in=schemas.ModelConfigCreate(
                configuration=encoders.jsonable_encoder(
                    obj=impl.ModelCreateImpl(
                        name=file_name,
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
    else:
        LOGGER.info('Adding binary for model %s', model_id)
        model = crud.model.get(db, id=model_id)
        if not model:
            raise fastapi.HTTPException(status_code=422, detail='Model not exist')

    model_config = crud.model_config.get(db, id=model.id)
    if not model_config:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model configuration not exist')

    endpoint = crud.endpoint.get(db, id=model.id)
    if not endpoint:
        LOGGER.info('Endpoint not exist, creating')
        # Creation
        crud.endpoint.create_with_model_and_binary(
            db,
            model_id=model.id,
            ec=schemas.EndpointCreate(name=model_config.configuration['name']),
            bc=schemas.BinaryMlModelCreate(
                model_b64=model_binary,
                input_data_structure=input_data_structure,
                output_data_structure=output_data_structure,
                format=format_))
        return model.id
    else:
        LOGGER.warning('Endpoint already exists, existing binary upload')
        raise fastapi.HTTPException(status_code=422, detail='Endpoint already exists')
