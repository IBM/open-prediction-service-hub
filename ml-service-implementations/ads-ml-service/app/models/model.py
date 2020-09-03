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


import sqlalchemy as sa
import sqlalchemy.orm as orm

import app.db.base_class as base_class


class Model(base_class.Base):
    name = sa.Column('name', sa.NCHAR(length=128), nullable=False, index=True, unique=True)

    config = orm.relationship('ModelConfig', back_populates='model', cascade='all, delete', uselist=False)
    endpoint = orm.relationship('Endpoint', back_populates='model', cascade='all, delete')
