#!/usr/bin/env python3


from sqlalchemy import Column, String, JSON, LargeBinary, Integer, ForeignKey
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    configuration = Column(JSON, nullable=False)

    binary_id = Column(Integer, ForeignKey('binary_ml_model.id'))
    binary = relationship('BinaryMLModel', back_populates='model_metadata', uselist=False)

    __table_args__ = (
        UniqueConstraint('name', 'version', name='_unique_name_ver_combination'),
        Index('_name_ver_composite_index', 'name', 'version'),
    )


class BinaryMLModel(Base):
    __tablename__ = "binary_ml_model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    model_b64 = Column(LargeBinary, nullable=False)

    model_metadata = relationship('Model', back_populates='binary', uselist=False)
