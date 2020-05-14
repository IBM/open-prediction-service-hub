#!/usr/bin/env python3
import os
import pickle
import unittest
from tempfile import TemporaryDirectory
from typing import Dict, Text, Any

from dynamic_hosting.core import Model as MLModel
from dynamic_hosting.core.configuration import ServerConfiguration
from dynamic_hosting.core.util import obj_to_base64
from dynamic_hosting.db import models
from dynamic_hosting.db.crud import create_model, delete_model, read_models, read_model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.prepare_models import miniloan_rfc_pickle, miniloan_lr_pickle, miniloan_rfr_pickle


class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()
        os.environ['model_storage'] = str(self.tmp_dir.name)
        engine = create_engine(
                f'sqlite:///{ServerConfiguration().model_storage.joinpath("EML.db")}',
                connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        self.db = SessionLocal()
        models.Base.metadata.create_all(bind=engine)

    def tearDown(self) -> None:
        self.db.close()
        self.tmp_dir.cleanup()

    def test_add_model(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m: MLModel = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))
        create_model(self.db, m)

        self.assertEqual(1, len(read_models(self.db)))

    def test_get_models(self):
        self.assertEqual(0, len(read_models(self.db)))

        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m: MLModel = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))
        create_model(self.db, m)

        self.assertEqual(1, len(read_models(self.db)))

    def test_get_model(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m1 = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))

        create_model(self.db, m1)

        item = read_model(self.db, model_name=m1.name, model_version=m1.version)
        self.assertEqual(m1, MLModel(model=item.model_b64, **item.configuration))

    def test_delete_model(self):
        self.assertEqual(0, len(read_models(self.db)))

        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m1 = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))
        with miniloan_lr_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m2 = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))
        with miniloan_rfr_pickle().open(mode='rb') as fd:
            contents: Dict[Text, Any] = pickle.loads(fd.read())
        m3 = MLModel(model=obj_to_base64(contents.get('model')), **contents.get('model_config'))

        create_model(self.db, m1)
        create_model(self.db, m2)
        create_model(self.db, m3)

        self.assertEqual(3, len(read_models(self.db)))

        delete_model(self.db, model_name=m1.name)
        self.assertEqual(2, len(read_models(self.db)))
        # delete deleted model
        delete_model(self.db, model_name=m1.name)
        self.assertEqual(2, len(read_models(self.db)))

        delete_model(self.db, model_name=m2.name, model_version=m2.version)
        self.assertEqual(1, len(read_models(self.db)))

        delete_model(self.db, model_name=m3.name)
        self.assertEqual(0, len(read_models(self.db)))
