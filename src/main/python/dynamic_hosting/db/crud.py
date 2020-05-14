#!/usr/bin/env python3


from typing import Text, List, Optional, NoReturn

from sqlalchemy.orm import Session

from . import models
from ..core import model


def read_model(db: Session, model_name: Text, model_version: Text) -> Optional[models.Model]:
    return db.query(models.Model).filter(models.Model.name == model_name, models.Model.version == model_version).first()


def read_models(db: Session) -> List[models.Model]:
    return db.query(models.Model).all()


def create_model(db: Session, ml_model: model.Model) -> NoReturn:
    db.add(
        models.Model(
            name=ml_model.name, version=ml_model.version,
            configuration=ml_model.get_meta_model().dict(), model_b64=ml_model.model)
    )
    db.commit()


def delete_model(db: Session, model_name: Text, model_version: Optional[Text] = None) -> NoReturn:
    if model_version is None:
        db.query(models.Model).filter(models.Model.name == model_name).delete()
    else:
        db.query(models.Model).filter(models.Model.name == model_name, models.Model.version == model_version).delete()
    db.commit()
