#!/usr/bin/env python3
import pickle
from typing import Text, List, Optional, NoReturn

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models as db_model
from ..schemas import model as ops_model


def read_model(db: Session, model_name: Text, model_version: Text) -> Optional[ops_model.Model]:
    m: db_model.Model = db.query(db_model.Model)\
        .filter(db_model.Model.name == model_name, db_model.Model.version == model_version)\
        .first()
    return ops_model.Model(model=pickle.loads(m.binary.model_b64), info=ops_model.MLSchema(**m.configuration))


def read_model_schemas(db: Session) -> List[ops_model.MLSchema]:
    return [ops_model.MLSchema(**conf[0]) for conf in db.query(db_model.Model.configuration).all()]


def count_models(db: Session) -> int:
    return db.query(db_model.Model).count()


def create_model(db: Session, ml_model: ops_model.Model) -> NoReturn:
    db.add(
        db_model.Model(
            name=ml_model.info.name,
            version=ml_model.info.version,
            configuration=ml_model.info.dict(),
            binary=db_model.BinaryMLModel(
                model_b64=pickle.dumps(ml_model.model)
            )
        )
    )
    db.commit()


def delete_model(db: Session, model_name: Text, model_version: Optional[Text] = None) -> NoReturn:
    if model_version is None:
        db.query(db_model.Model).filter(db_model.Model.name == model_name).delete()
    else:
        db.query(db_model.Model)\
            .filter(and_(db_model.Model.name == model_name, db_model.Model.version == model_version)).delete()
    db.commit()
