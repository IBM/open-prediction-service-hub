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


import sqlalchemy as sql

import app.db.base_class as base_class


class User(base_class.Base):
    id = sql.Column('id', sql.Integer, nullable=False, unique=True, index=True, primary_key=True)
    username = sql.Column(sql.NCHAR(32), nullable=False, index=True, unique=True)
    hashed_password = sql.Column(sql.BINARY(64), nullable=False)
