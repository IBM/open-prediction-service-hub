#!/usr/bin/env python3
import pickle
from typing import Text, List, Optional, NoReturn

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models
from ..core import model


def read_model(db: Session, model_name: Text, model_version: Text) -> Optional[models.Model]:
    return db.query(models.Model).filter(models.Model.name == model_name, models.Model.version == model_version).first()


def read_models(db: Session) -> List[models.Model]:
    return db.query(models.Model).all()


def count_models(db: Session) -> int:
    return db.query(models.Model).count()


def create_model(db: Session, ml_model: model.Model) -> NoReturn:
    db.add(
        models.Model(
            name=ml_model.info.name,
            version=ml_model.info.version,
            configuration=ml_model.info.dict(),
            model_b64=pickle.dumps(ml_model.model))
    )
    db.commit()


def delete_model(db: Session, model_name: Text, model_version: Optional[Text] = None) -> NoReturn:
    if model_version is None:
        db.query(models.Model).filter(models.Model.name == model_name).delete()
    else:
        tmp = db.query(models.Model).filter(and_(models.Model.name == model_name, models.Model.version == model_version))
        tmp.delete()
    db.commit()
