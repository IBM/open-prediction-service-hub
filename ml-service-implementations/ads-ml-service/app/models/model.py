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


from sqlalchemy import Column, String
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Model(Base):

    name = Column(String, nullable=False)
    version = Column(String, nullable=False)

    binary = relationship('BinaryMLModel', back_populates='model', uselist=False, cascade='all, delete')
    config = relationship('ModelConfig', back_populates='model', uselist=False, cascade='all, delete')

    __table_args__ = (
        UniqueConstraint('name', 'version', name='_unique_name_ver_combination'),
        Index('_name_ver_composite_index', 'name', 'version'),
    )
