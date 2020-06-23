#!/usr/bin/env python3
import pickle
from typing import Text, List, Optional, NoReturn

from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..schemas import model as ops_model

from ..models import model_config
from ..models import binary_ml_model


def read_model(db: Session, model_name: Text, model_version: Text) -> Optional[ops_model.Model]:
    m: model_config.ModelConfig = db.query(model_config.ModelConfig)\
        .filter(model_config.ModelConfig.name == model_name, model_config.ModelConfig.version == model_version)\
        .first()
    return ops_model.Model(model=pickle.loads(m.binary.model_b64), info=ops_model.MLSchema(**m.configuration))


def read_model_schemas(db: Session) -> List[ops_model.MLSchema]:
    return [ops_model.MLSchema(**conf[0]) for conf in db.query(model_config.ModelConfig.configuration).all()]


def count_models(db: Session) -> int:
    return db.query(model_config.ModelConfig).count()


def create_model(db: Session, ml_model: ops_model.Model) -> NoReturn:
    db.add(
        model_config.ModelConfig(
            name=ml_model.info.name,
            version=ml_model.info.version,
            configuration=ml_model.info.dict(),
            binary=binary_ml_model.BinaryMLModel(
                model_b64=pickle.dumps(ml_model.model)
            )
        )
    )
    db.commit()


def delete_model(db: Session, model_name: Text, model_version: Optional[Text] = None) -> NoReturn:
    if model_version is None:
        db.query(model_config.ModelConfig).filter(model_config.ModelConfig.name == model_name).delete()
    else:
        db.query(model_config.ModelConfig)\
            .filter(and_(model_config.ModelConfig.name == model_name, model_config.ModelConfig.version == model_version)).delete()
    db.commit()
