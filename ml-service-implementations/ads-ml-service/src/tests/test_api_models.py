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


from __future__ import annotations

import pickle
import unittest
from pathlib import Path
from typing import List, Text

import numpy as np
from predictions.schemas.model import Model
from predictions.core.feature import Feature
from predictions.schemas.prediction import Prediction, Probability
from sklearn.svm import LinearSVC
from .prepare_models import miniloan_linear_svc_pickle


class TestFeature(unittest.TestCase):
    def test_int_feature(self):
        int_type_alias: List[Text] = [
            'int',  # native python int
            'byte',
            'ubyte',
            'short',
            'ushort',
            'intc',
            'uintc',
            'int_',
            'uint',
            'longlong',
            'ulonglong',
            'int8',
            'int16',
            'int32',
            'int64',
            'uint8',
            'uint16',
            'uint32',
            'uint64',
        ]

        self.assertTrue(
            all(
                (f.get_type() for f in (Feature(name='f{i}'.format(i=i), order=i, type=val) for i, val in enumerate(
                    int_type_alias)))
            )
        )

    def test_bool_feature(self):
        bool_type_alias: List[Text] = [
            'bool',  # native python bool
            'bool_'
        ]

        self.assertTrue(
            all(
                (f.get_type() for f in (Feature(name='f{i}'.format(i=i), order=i, type=val) for i, val in enumerate(
                    bool_type_alias)))
            )
        )

    def test_float_feature(self):
        bool_type_alias: List[Text] = [
            'float',  # native python float
            'half',
            'float16',
            'single',
            'double',
            'longdouble',
            'float32',
            'float64',
            'float_'
        ]

        self.assertTrue(
            all(
                (f.get_type() for f in (Feature(name='f{i}'.format(i=i), order=i, type=val) for i, val in enumerate(
                    bool_type_alias)))
            )
        )

    def test_nominal_feature(self):
        nominal_type_alias: List[Text] = [
            'str',  # native python str
            'string_',
            'unicode_'
        ]

        self.assertTrue(
            all(
                (f.get_type() for f in (Feature(name='f{i}'.format(i=i), order=i, type=val) for i, val in enumerate(
                    nominal_type_alias)))
            )
        )

    def test_not_existing_type(self):
        self.assertRaises(ValueError, Feature, name='not_valid', order=0, type='unknown')


class TestPrediction(unittest.TestCase):
    def test_not_valid_predict_proba(self):
        self.assertRaises(ValueError, Prediction, prediction='error', probabilities=[
            Probability(class_name=f'n{i}', class_index=i, value=val) for i, val in enumerate(
                np.random.dirichlet(np.ones(10), size=1)[0] / 2)
        ]
                          )

    def test_valid_predict_proba(self):
        Prediction(prediction='good', probabilities=[
            Probability(class_name=f'n{i}', class_index=i, value=val) for i, val in enumerate(
                np.random.dirichlet(np.ones(10), size=1)[0])
        ]
                   )


class TestFromPickle(unittest.TestCase):

    def setUp(self) -> None:
        self.pkl: Path = miniloan_linear_svc_pickle()

    def test_import(self):
        with self.pkl.open(mode='rb') as fd:
            content: bytes = fd.read()

        model: Model = Model.from_pickle(
                pickle_file=content,
                model_name='model',
                metadata_name='model_config'
            )

        self.assertEqual(LinearSVC, type(pickle.loads(model.model)))
