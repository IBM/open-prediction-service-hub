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

import sqlalchemy.orm as orm

import app.crud as crud
import app.schemas as schemas
import app.tests.utils.utils as utils


def test_create_endpoint(
        db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]
) -> typing.NoReturn:
    endpoint_name = utils.random_string()
    model = crud.model.create(db, obj_in=schemas.ModelCreate(name=classification_config['name']))
    endpoint_in = schemas.EndpointCreate(name=endpoint_name)
    endpoint = crud.endpoint.create_with_model(db, obj_in=endpoint_in, model_id=model.id)

    assert endpoint.name == endpoint_name
    assert endpoint.model_id == model.id
