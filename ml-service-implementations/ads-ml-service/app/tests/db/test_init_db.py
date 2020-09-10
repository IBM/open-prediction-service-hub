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


def test_load_models(
    db: orm.Session,
) -> typing.NoReturn:
    import app.db.init_db as init_db
    project_dir = init_db.EXAMPLES_ROOT.joinpath('classification', 'miniloan_linear_svc')
    init_db.load_models(db=db, project_dirs=[project_dir])
    model = crud.model.get_all(db)[0]

    assert model is not None
