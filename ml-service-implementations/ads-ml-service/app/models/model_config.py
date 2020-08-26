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


from sqlalchemy import Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ModelConfig(Base):
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship('Model', back_populates='config', uselist=False)

    configuration = Column(JSON, nullable=False)
