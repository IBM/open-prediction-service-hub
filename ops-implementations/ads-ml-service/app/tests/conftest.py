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
import pathlib
import typing

import fastapi.testclient as fastapi_testclient
import pytest
import sqlalchemy
import sqlalchemy.orm as sqlalchemy_orm
import yaml

import app.core.configuration as app_config
import app.crud as app_crud
import app.db.base as app_db_base
import app.schemas as app_schemas
import app.tests.utils.user as app_tests_user


@pytest.fixture
def db(tmp_path) -> typing.Iterable[sqlalchemy_orm.Session]:
    os.environ['MODEL_STORAGE'] = str(tmp_path.resolve())
    engine = sqlalchemy.create_engine(
        f'sqlite:///{tmp_path.resolve().joinpath("test.db")}', connect_args={"check_same_thread": False})
    app_db_base.Base.metadata.create_all(bind=engine)
    sm_instance = sqlalchemy_orm.sessionmaker(
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
def client(db, tmp_path) -> typing.Iterable[fastapi_testclient.TestClient]:
    logging_configs = yaml.safe_load(pathlib.Path(__file__).parents[2].joinpath('logging.yaml').read_text())
    logging_configs['handlers']['info_file_handler']['filename'] = tmp_path.joinpath('info.log').__str__()
    logging_configs['handlers']['error_file_handler']['filename'] = tmp_path.joinpath('error.log').__str__()
    os.environ['LOGGING'] = tmp_path.joinpath('logging.yaml').__str__()
    os.environ['SETTINGS'] = tmp_path.__str__()
    tmp_path.joinpath('logging.yaml').write_text(yaml.dump(logging_configs))

    user = app_crud.user.create(db, obj_in=app_schemas.UserCreate(
        username=app_config.get_config().DEFAULT_USER, password=app_config.get_config().DEFAULT_USER_PWD))
    assert user is not None, 'Default user can not be created'

    def _db_override():
        return db

    import app.main as app_main
    import app.api.deps as app_api_deps

    app = app_main.get_app()

    app.dependency_overrides[app_api_deps.get_db] = _db_override

    with fastapi_testclient.TestClient(app) as c:
        yield c


@pytest.fixture
def user_token_header(client, db) -> typing.Dict[typing.Text, typing.Text]:
    return app_tests_user.auth_token_from_username(
        client=client,
        db=db,
        username=app_config.get_config().USERNAME_TEST_USER
    )
