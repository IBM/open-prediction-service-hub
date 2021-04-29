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
import sqlalchemy.orm as saorm
import starlette.status as status

import app.crud as crud
import app.runtime.inspection as app_signature_inspection
import app.runtime.wrapper as app_runtime_wrapper
import app.schemas as schemas
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as impl

router = fastapi.APIRouter()
LOGGER = logging.getLogger(__name__)

SUPPORTED_FORMATS = ('.pmml',)


def is_compatible(
        model: bytes,
        format_: app_binary_config.ModelWrapper
) -> bool:
    # noinspection PyBroadException
    try:
        app_runtime_wrapper.ModelInvocationExecutor(
            model=model,
            input_type=app_binary_config.ModelInput.AUTO,
            output_type=app_binary_config.ModelOutput.AUTO,
            binary_format=format_
        )
    except Exception:
        return False
    return True


def store_model(
        db: saorm.Session,
        model_binary: bytes,
        input_data_structure: app_binary_config.ModelInput = None,
        output_data_structure: app_binary_config.ModelOutput = None,
        format_: app_binary_config.ModelWrapper = None,
        model_id: typing.Optional[int] = None,
        name: typing.Optional[str] = None
) -> int:
    if not ((model_id is None) ^ (name is None)):
        raise RuntimeError('`model_id` xor `name` needs to be true')

    if model_id is None:
        LOGGER.info('Adding binary directly')

        input_schema_pmml = app_signature_inspection.inspect_pmml_input(model_binary)
        output_schema_pmml = app_signature_inspection.inspect_pmml_output(model_binary)

        input_schema_ops = None if not input_schema_pmml else [
                            impl.FeatureImpl(
                                name=k,
                                order=i,
                                type=input_schema_pmml[k]
                            ) for i, k in enumerate(input_schema_pmml.keys())
                        ]
        output_schema_ops = None if not output_schema_pmml else {
                            k: {
                                'type': v
                            }
                            for k, v in output_schema_pmml.items()
                        }

        model = crud.model.create(db, obj_in=schemas.ModelCreate())
        crud.model_config.create_with_model(
            db,
            obj_in=schemas.ModelConfigCreate(
                configuration=encoders.jsonable_encoder(
                    obj=impl.ModelCreateImpl(
                        name=name,
                        input_schema=input_schema_ops,
                        output_schema=output_schema_ops
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
