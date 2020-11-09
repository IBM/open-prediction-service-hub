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


import os
import pickle
import random
import typing
from typing import NoReturn, Dict, Generator, Text

import numpy as np
import pytest
import sqlalchemy.orm as orm
import xgboost as xgb
from fastapi.testclient import TestClient
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.core.supported_lib as supported_lib
import app.models as models
import app.schemas as schemas
import app.tests.utils.utils as utils
from app import crud
from app.core.configuration import get_config
from app.db.base import Base
from app.schemas import UserCreate
from app.tests.utils.user import auth_token_from_username
from app.tests.utils.utils import random_string


class DummyRegressor(BaseEstimator, RegressorMixin):
    def __init__(self):
        pass

    def fit(self, x, y) -> NoReturn:
        x_, y_ = check_X_y(x, y)
        setattr(self, 'range_', (min(y_), max(y_)))

    def predict(self, x) -> np.ndarray:
        """
        x is an array-like object
        """
        check_is_fitted(self, attributes=['range_'])
        check_array(x)
        r = getattr(self, 'range_')
        return np.array([random.uniform(a=r[0], b=r[1]) for _ in range(len(x))])


@pytest.fixture
def regression_predictor():
    regressor = DummyRegressor()
    data = np.random.rand(10, 3)
    regressor.fit(data[:, :1], data[:, 2])
    return regressor


class DummyClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, x, y) -> NoReturn:
        x_, y_ = check_X_y(x, y)
        setattr(self, 'unique_', np.unique(y_))

    def predict(self, x) -> np.ndarray:
        """
        x is an array-like object
        """
        check_is_fitted(self, attributes=['unique_'])
        check_array(x)
        u = getattr(self, 'unique_')
        return np.array([random.choice(u) for _ in range(len(x))])


@pytest.fixture
def classification_predictor() -> object:
    classifier = DummyClassifier()
    x_random = np.random.rand(10, 2)
    y_random = np.array([random_string() for _ in range(10)])
    classifier.fit(x_random, y_random)
    return classifier


@pytest.fixture
def xgb_classification_predictor() -> xgb.XGBClassifier:
    classifier = xgb.XGBClassifier(random_state=42)
    x_random = np.random.rand(10, 2)
    y_random = np.array([random_string() for _ in range(10)])
    classifier.fit(x_random, y_random)
    return classifier


class DummyClassifierProb(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, x, y) -> NoReturn:
        x_, y_ = check_X_y(x, y)
        setattr(self, 'unique_', np.unique(y_))

    def predict(self, x) -> np.ndarray:
        """
        x is an array-like object
        """
        check_is_fitted(self, attributes=['unique_'])
        check_array(x)
        u = getattr(self, 'unique_')
        return np.array([random.choice(u) for _ in range(len(x))])

    def predict_proba(self, x) -> np.ndarray:
        """
        x is an array-like object
        """
        check_is_fitted(self, attributes=['unique_'])
        check_array(x)
        u = getattr(self, 'unique_')
        return np.array([np.random.dirichlet(np.ones(len(u)), size=1)[0] for _ in range(len(x))])


@pytest.fixture
def classification_with_prob_predictor():
    classifier = DummyClassifierProb()
    x_random = np.random.rand(10, 2)
    y_random = np.array([random_string() for _ in range(10)])
    classifier.fit(x_random, y_random)
    return classifier


@pytest.fixture
def base_config() -> Dict:
    config_v2 = {
        'name': random_string(),
        'version': '0.0.1',
        'input_schema': [
            {
                'name': 'x',
                'order': 0,
                'type': 'double'
            },
            {
                'name': 'y',
                'order': 1,
                'type': 'double'
            }
        ],
        'output_schema': {
            'prediction': {
                'type': 'string'
            },
            'probability': {
                'type': 'array',
                'items': 'double'
            },
            'timeElapsed': {
                'type': 'string',
                'format': 'date-time'
            },
            'inError': {
                'type': 'boolean'
            }
        },
        'metadata': {
            'description': random_string(),
            'author': random_string(),
            'metrics': [
                {
                    'name': random_string(),
                    'value': 0.97
                }
            ]
        }

    }
    return config_v2


@pytest.fixture
def classification_config(base_config: Dict) -> Dict:
    base_config['output_schema'] = {
        'attributes': [
            {'name': 'prediction', 'type': 'string'}
        ]
    }
    return base_config


@pytest.fixture
def regression_config(base_config: Dict) -> Dict:
    base_config['method_name'] = 'predict'
    base_config['output_schema'] = {
        'attributes': [
            {'name': 'prediction', 'type': 'float'}
        ]
    }
    return base_config


@pytest.fixture
def classification_prob_config(base_config: Dict) -> Dict:
    base_config['method_name'] = 'predict_proba'
    base_config['output_schema'] = {
        'attributes': [
            {'name': 'prediction', 'type': 'float'},
            {'name': 'probabilities', 'type': '[Probability]'}
        ]
    }
    return base_config


@pytest.fixture
def db(tmp_path) -> Generator[Session, None, None]:
    os.environ['MODEL_STORAGE'] = str(tmp_path.resolve())
    engine = create_engine(
        f'sqlite:///{tmp_path.resolve().joinpath("test.db")}', connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    sm_instance = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = sm_instance()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db, tmp_path) -> Generator[TestClient, None, None]:
    os.environ['DEFAULT_USER'] = get_config().DEFAULT_USER
    os.environ['DEFAULT_USER_PWD'] = get_config().DEFAULT_USER

    user = crud.user.create(db, obj_in=UserCreate(
        username=get_config().DEFAULT_USER, password=get_config().DEFAULT_USER_PWD))
    assert user is not None, 'Default user can not be created'

    def _db_override():
        return db

    from app.main import get_app
    from app.api.deps import get_db

    app = get_app()

    app.dependency_overrides[get_db] = _db_override

    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_token_header(client, db) -> Dict[Text, Text]:
    return auth_token_from_username(client=client, db=db, username=get_config().USERNAME_TEST_USER)


@pytest.fixture
def endpoint_with_model(
        db: orm.Session,
        classification_config: typing.Dict[typing.Text, typing.Any],
) -> models.Endpoint:
    model = crud.model.create(db, obj_in=schemas.ModelCreate(name=classification_config['name']))
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=classification_config), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(
        db, obj_in=schemas.EndpointCreate(name=utils.random_string()), model_id=model.id
    )
    return endpoint


@pytest.fixture
def endpoint_with_model_and_binary(
        db: orm.Session,
        endpoint_with_model: models.Endpoint,
        classification_predictor: object,
) -> models.Endpoint:
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(obj=classification_predictor),
        library=supported_lib.MlLib.SKLearn
    ), endpoint_id=endpoint_with_model.id)
    return endpoint_with_model


class IdentityPredictor(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, x, y) -> NoReturn:
        pass

    def predict(self, x) -> typing.Any:
        return x


@pytest.fixture
def endpoint_with_identity_predictor(
        db: orm.Session,
        endpoint_with_model: models.Endpoint,
        classification_predictor: object,
) -> models.Endpoint:
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(obj=IdentityPredictor()),
        library=supported_lib.MlLib.SKLearn
    ), endpoint_id=endpoint_with_model.id)
    return endpoint_with_model


@pytest.fixture
def endpoint_with_xgb_predictor(
        tmpdir,
        db: orm.Session,
        endpoint_with_model: models.Endpoint,
        xgb_classification_predictor: xgb.XGBClassifier,
) -> models.Endpoint:
    model_path = tmpdir.join('model.bst')
    xgb_classification_predictor.save_model(fname=model_path.__str__())
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=model_path.read_binary(),
        library=supported_lib.MlLib.XGBoost
    ), endpoint_id=endpoint_with_model.id)
    return endpoint_with_model
