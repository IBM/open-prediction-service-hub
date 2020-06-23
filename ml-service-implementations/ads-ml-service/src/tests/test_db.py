#!/usr/bin/env python3
import os
import pickle
import unittest
from tempfile import TemporaryDirectory
from typing import Dict, Text, Any

from predictions.core.model import Model as MLModel
from predictions.core.configuration import ServerConfiguration
from predictions.schemas.model import MLSchema
from predictions.db.base import Base
from predictions.db.crud import create_model, delete_model, read_model_schemas, read_model, count_models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .prepare_models import miniloan_rfc_pickle, miniloan_linear_svc_pickle, miniloan_rfr_pickle


class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()
        os.environ['MODEL_STORAGE'] = str(self.tmp_dir.name)
        engine = create_engine(
                f'sqlite:///{ServerConfiguration().MODEL_STORAGE.joinpath("EML.db")}',
                connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        self.db = SessionLocal()
        Base.metadata.create_all(bind=engine)

    def tearDown(self) -> None:
        self.db.close()
        self.tmp_dir.cleanup()

    def test_add_model(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m: MLModel = MLModel(model=contents.get('model'), info=MLSchema(**contents.get('model_config')))
        create_model(self.db, m)

        self.assertEqual(1, count_models(self.db))

    def test_count_models(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m: MLModel = MLModel(model=contents.get('model'), info=MLSchema(**contents.get('model_config')))
        create_model(self.db, m)

        self.assertEqual(1, count_models(db=self.db))

    def test_get_models(self):
        self.assertEqual(0, count_models(self.db))

        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m: MLModel = MLModel(model=pickle.dumps(contents.get('model')), info=MLSchema(**contents.get('model_config')))
        create_model(self.db, m)

        self.assertEqual(1, count_models(self.db))

    def test_get_model(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m1 = MLModel(model=pickle.dumps(contents.get('model')), info=MLSchema(**contents.get('model_config')))

        create_model(self.db, m1)

        self.assertEqual(m1.info, read_model(self.db, model_name=m1.info.name, model_version=m1.info.version).info)

    def test_delete_model(self):
        self.assertEqual(0, count_models(self.db))

        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
            m1 = MLModel(model=contents.get('model'), info=MLSchema(**contents.get('model_config')))
        with miniloan_linear_svc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
            m2 = MLModel(model=contents.get('model'), info=MLSchema(**contents.get('model_config')))
        with miniloan_rfr_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
            m3 = MLModel(model=contents.get('model'), info=MLSchema(**contents.get('model_config')))

        create_model(self.db, m1)
        create_model(self.db, m2)
        create_model(self.db, m3)

        self.assertEqual(3, count_models(self.db))

        delete_model(self.db, model_name=m1.info.name)
        self.assertEqual(2, count_models(self.db))
        # delete deleted model
        delete_model(self.db, model_name=m1.info.name)
        self.assertEqual(2, count_models(self.db))

        delete_model(self.db, model_name=m2.info.name, model_version=m2.info.version)
        self.assertEqual(1, count_models(self.db))

        delete_model(self.db, model_name=m3.info.name)
        self.assertEqual(0, count_models(self.db))
