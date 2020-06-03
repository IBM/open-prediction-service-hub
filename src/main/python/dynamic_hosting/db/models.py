#!/usr/bin/env python3


from sqlalchemy import Column, String, JSON, LargeBinary, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
    __tablename__ = "model"

    #id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String, nullable=False, primary_key=True, index=True)
    version = Column(String, nullable=False, primary_key=True, index=True)
    model_b64 = Column(LargeBinary, nullable=False)
    configuration = Column(JSON, nullable=False)


# class BinaryMLModel(Base):
#     __tablename__ = "binary_ml_model"
#
#     id = Column(Integer, nullable=False, primary_key=True, index=True)
#     model_b64 = Column(LargeBinary, nullable=False)
