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


import pickle

from fastapi.encoders import jsonable_encoder

from ....schemas.binary_ml_model import BinaryMLModelCreate
from ....schemas.model import ModelCreate
from ....schemas.model_config import ModelConfigCreate
from ....core.configuration import get_config
from .... import crud

API_VER = '/v1'


def test_open_api_doc(client):
    response = client.get(url='/open-prediction-service.json')
    assert response.status_code == 200


def test_get_server_status(client):
    response = client.get(url=get_config().API_V1_STR + '/status')
    assert response.status_code == 200
    assert response.json().get('model_count') == 0


def test_get_models(db, classification_predictor, classification_config, client):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    response = client.get(url=get_config().API_V1_STR + '/models')

    assert response.status_code == 200
    assert response.json() is not None
    assert jsonable_encoder(response.json()[0]) == jsonable_encoder(model.config.configuration)


def test_add_models(db, classification_predictor, classification_config, client):
    archive = {
        'model': classification_predictor,
        'model_config': classification_config
    }
    response = client.post(
        get_config().API_V1_STR + '/models',
        files={'file': pickle.dumps(archive)}
    )

    model = crud.crud_model.model.get_by_name_and_ver(
        db, name=classification_config['name'], version=classification_config['version'])

    assert response.status_code == 200
    assert model is not None


def test_delete_model(db, classification_predictor, classification_config, client):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    client.delete(
        url=get_config().API_V1_STR + '/models',
        params={'model_name': model.name, 'model_version': model.version}
    )

    model_1 = crud.crud_model.model.get(db, id=model.id)

    assert model_1 is None
