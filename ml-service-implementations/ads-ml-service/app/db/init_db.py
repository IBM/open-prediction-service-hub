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


import json
import logging
import pathlib
import subprocess
import typing as typ

import yaml
import fastapi.encoders as encoders
import sqlalchemy.orm as saorm

import app.core.configuration as conf
import app.core.supported_lib as supported_lib
import app.crud as crud
import app.db.base as db_base
import app.db.session as db_session
import app.gen.schemas.ops_schemas as ops_schemas
import app.schemas as schemas
import app.schemas.impl as impl

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2].resolve()
EXAMPLES_ROOT = PROJECT_ROOT.joinpath('examples', 'model_training_and_deployment')
MODEL_BASENAME = 'model'
MODEL_EXTENSIONS = ['.joblib', '.pkl', '.pickle', '.bst']

logger = logging.getLogger(__name__)


def train_example_model(project_dir: pathlib.Path) -> pathlib.Path:
    paths = [project_dir.joinpath(MODEL_BASENAME + model_extension) for model_extension in MODEL_EXTENSIONS]
    try:
        model_file = next(path for path in paths if path.exists())
        if not conf.get_config().RETRAIN_MODELS:
            logger.info(f'model {model_file} exists. set RETRAIN_MODELS to re-train.')
            return model_file
        else:
            logger.info(f'model {model_file} exists, re-training it.')
    except StopIteration:
        logger.info(f'model for {project_dir} doesn\'t exists, training.')

    # input/output is accepted as str instead of bytes
    subprocess.run(
        ['python3', str(project_dir.joinpath('training.py'))],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return next(path for path in paths if path.exists())


def find_config_file(project_dir: pathlib.Path) -> pathlib.Path:
    model_config = project_dir.joinpath('deployment_conf.json')
    if model_config.exists():
        return model_config
    else:
        raise ValueError(f'Configuration file not found in: {project_dir}')


def load_models(
        db: saorm.Session, project_dirs: typ.List[pathlib.Path]
) -> typ.List[typ.Tuple[pathlib.Path, pathlib.Path, pathlib.Path]]:
    projects = list(
        map(lambda project: (project, train_example_model(project), find_config_file(project)), project_dirs))

    for p in projects:
        binary: bytes
        config: typ.Dict[typ.Text, typ.Any]
        with p[1].open(mode='rb') as fd:
            binary = fd.read()
        with p[2].open(mode='r') as fd:
            config = json.load(fd)

        model_config = impl.ModelCreateImpl(**config['model'])
        endpoint_config = ops_schemas.EndpointCreation(
            **config['endpoint']
        )
        model = crud.model.create(db, obj_in=schemas.ModelCreate())
        model_config = crud.model_config.create_with_model(
            db,
            obj_in=schemas.ModelConfigCreate(configuration=encoders.jsonable_encoder(obj=model_config)),
            model_id=model.id
        )
        endpoint = crud.endpoint.create_with_model(
            db,
            obj_in=schemas.EndpointCreate(name=endpoint_config.name),
            model_id=model.id
        )
        lib = supported_lib.MlLib[config['binary']['lib']]
        bin_db = crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
            model_b64=binary,
            library=lib
        ), endpoint_id=endpoint.id)

        assert all(obj for obj in (model, model_config, endpoint, bin_db))
    return projects


def init_db(db: saorm.Session):
    db_base.Base.metadata.create_all(bind=db_session.engine)

    with PROJECT_ROOT.joinpath('preload-conf.yaml').open(mode='r') as fd:
        preload_conf = yaml.load(fd, yaml.SafeLoader)

    if preload_conf.get('models') is not None and len(preload_conf.get('models')) > 0:
        # load example ml model
        load_models(
            db, [
                 PROJECT_ROOT.joinpath(p) for p in preload_conf.get('models')
            ]
        )

    user = crud.user.get_by_username(db, username=conf.get_config().DEFAULT_USER)
    if user is None:
        user_in = schemas.user.UserCreate(
            username=conf.get_config().DEFAULT_USER,
            password=conf.get_config().DEFAULT_USER_PWD
        )
        crud.user.create(db, obj_in=user_in)
