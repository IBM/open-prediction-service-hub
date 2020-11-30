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


import re
from typing import Text

import sqlalchemy as sql
import sqlalchemy.ext.declarative as sql_declarative


@sql_declarative.as_declarative()
class Base:
    # id = sql.Column('id', sql.Integer, nullable=False, unique=True, index=True, primary_key=True)
    __table_name_pattern__ = re.compile(r'(?<!^)(?=[A-Z])')

    @sql_declarative.declared_attr
    def __tablename__(cls) -> Text:
        return Base.__table_name_pattern__.sub('_', cls.__name__).lower()
