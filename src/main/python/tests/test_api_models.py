#!/usr/bin/env python3

from __future__ import annotations

import unittest
from typing import List, Text, Type

from dynamic_hosting.core.feature import Feature
from dynamic_hosting.openapi.response import Prediction, FeatProbaPair

import numpy as np


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
            FeatProbaPair(name='n{i}'.format(i=i), proba=val) for i, val in enumerate(
                np.random.dirichlet(np.ones(10), size=1)[0]/2)
            ]
        )

    def test_valid_predict_proba(self):
        Prediction(prediction='good', probabilities=[
            FeatProbaPair(name='n{i}'.format(i=i), proba=val) for i, val in enumerate(
                np.random.dirichlet(np.ones(10), size=1)[0])
            ]
        )
