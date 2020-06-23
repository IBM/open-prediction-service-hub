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


import pickle
from typing import Text, List, Optional, NoReturn

from sqlalchemy.orm import Session

from .. import models
from .. import schemas


def read_model(
        db: Session, model_name: Text,
        model_version: Text
) -> Optional[schemas.model.Model]:
    m: models.model_config.ModelConfig = db \
        .query(models.model_config.ModelConfig) \
        .filter(
            models.model_config.ModelConfig.name == model_name,
            models.model_config.ModelConfig.version == model_version) \
        .first()
    return schemas.model.Model(model=pickle.loads(m.binary.model_b64), info=schemas.model.MLSchema(**m.configuration))


def read_model_schemas(db: Session) -> List[schemas.model.MLSchema]:
    return [
        schemas.model.MLSchema(**conf[0]) for conf in db.query(models.model_config.ModelConfig.configuration).all()
    ]


def count_models(db: Session) -> int:
    return db.query(models.model_config.ModelConfig).count()


def create_model(db: Session, ml_model: schemas.model.Model) -> NoReturn:
    db.add(
        models.model_config.ModelConfig(
            name=ml_model.info.name,
            version=ml_model.info.version,
            configuration=ml_model.info.dict(),
            binary=models.binary_ml_model.BinaryMLModel(
                model_b64=pickle.dumps(ml_model.model)
            )
        )
    )
    db.commit()


def delete_model(db: Session, model_name: Text, model_version: Optional[Text] = None) -> NoReturn:
    if model_version is None:
        db.query(models.model_config.ModelConfig).filter(models.model_config.ModelConfig.name == model_name).delete()
    else:
        db \
            .query(models.model_config.ModelConfig) \
            .filter(
                models.model_config.ModelConfig.name == model_name,
                models.model_config.ModelConfig.version == model_version) \
            .delete()
    db.commit()
