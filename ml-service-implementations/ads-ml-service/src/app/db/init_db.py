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
import pickle
import subprocess
from pathlib import Path

from sqlalchemy.orm import Session

from .base import Base
from .session import engine
from .. import crud
from .. import schemas
from ..core.configuration import get_config
from ..schemas.binary_ml_model import BinaryMLModelCreate
from ..schemas.model import ModelCreate
from ..schemas.model_config import ModelConfigCreate

PROJECT_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_ROOT = PROJECT_ROOT.joinpath('examples')


def __prepare_archive(directory: Path, archive: Path) -> Path:
    logger = logging.getLogger(__name__)

    if archive.exists():
        if not get_config().RETRAIN_MODELS:
            logger.info(f'model {archive} exists. set RETRAIN_MODELS to re-train.')
            return archive
        else:
            logger.info(f'model {archive} exists, re-training it.')
    else:
        logger.info(f'model {archive} doesn\'t exists, training it.')

    # input/output is accepted as str instead of bytes
    subprocess.run(
        ['python3', str(directory.joinpath('training.py'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    subprocess.run(
        ['python3', str(directory.joinpath('deployment.py'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return archive


def __miniloan_linear_svc_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification', 'miniloan_linear_svc')
    archive = directory.joinpath('miniloan-linear-svc-archive.pkl')

    return __prepare_archive(directory, archive)


def __miniloan_xgb_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification', 'miniloan_xgb')
    archive = directory.joinpath('miniloan-xgb-archive.pkl')

    return __prepare_archive(directory, archive)


def __miniloan_rfc_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification_with_probabilities', 'miniloan_rfc')
    archive = directory.joinpath('miniloan-rfc-archive.pkl')

    return __prepare_archive(directory, archive)


def __miniloan_rfr_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath('model_training_and_deployment', 'regression', 'miniloan_rfr')
    archive = directory.joinpath('miniloan-rfr-archive.pkl')

    return __prepare_archive(directory, archive)


def __load_models(db: Session):
    __miniloan_linear_svc_pickle()
    __miniloan_xgb_pickle()
    __miniloan_rfc_pickle()
    __miniloan_rfr_pickle()

    models = PROJECT_ROOT.joinpath('examples').rglob('miniloan-*-archive.pkl')
    results = []
    for p in models:
        with p.open(mode='rb') as fd:
            content = fd.read()
            p = pickle.loads(content)
        predictor = p['model']
        config = p['model_config']

        binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(predictor))
        config_in = ModelConfigCreate(**config)

        model_in = ModelCreate(
            name=config['name'],
            version=config['version'],
            binary=binary_in,
            config=config_in
        )

        model = crud.crud_model.model.create(db, obj_in=model_in)
        results.append(model)

    assert (all(results))


def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    # load example ml model
    __load_models(db)

    user = crud.user.get_by_username(db, username=get_config().DEFAULT_USER)
    if user is None:
        user_in = schemas.user.UserCreate(
            username=get_config().DEFAULT_USER,
            password=get_config().DEFAULT_USER_PWD
        )
        user = crud.user.create(db, obj_in=user_in)
