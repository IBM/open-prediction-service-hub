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
import pathlib
import json

import sqlalchemy.orm as orm
import pytest

import app.crud as crud

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3].resolve()
EXAMPLES_ROOT = PROJECT_ROOT.joinpath('examples', 'model_training_and_deployment')


@pytest.mark.parametrize(
    'project_dir',
    [
        EXAMPLES_ROOT.joinpath('classification', 'iris_svc'),
        EXAMPLES_ROOT.joinpath('classification', 'miniloan_linear_svc'),
        EXAMPLES_ROOT.joinpath('classification', 'miniloan_xgb')
    ]
)
def test_load_models(
    db: orm.Session,
    project_dir: pathlib.Path
) -> typing.Any:
    import app.db.init_db as init_db
    loaded = init_db.load_models(db=db, project_dirs=[project_dir])
    with loaded[0][2].open(mode='r') as fd:
        config = json.load(fd)
    model = crud.model.get_by_name(db, name=config['model']['name'])

    assert model is not None
    assert model.config is not None
    assert all(
        [
            model.config.configuration[key] == config['model'][key] for key in config['model'].keys()
        ]
    )
    assert model.endpoint[0].name == config['endpoint']['name']
    assert model.endpoint[0].binary is not None
