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


from typing import Text, Type

import numpy as np
import pytest
from app.schemas.prediction import Prediction, Probability

from ...schemas.feature import Feature


@pytest.mark.parametrize(
    'type_str, real_type',
    [
        ('int', int),  # native python int
        ('byte', np.byte),
        ('ubyte', np.ubyte),
        ('short', np.short),
        ('ushort', np.ushort),
        ('intc', np.intc),
        ('uintc', np.uintc),
        ('int_', np.int_),
        ('uint', np.uint),
        ('longlong', np.longlong),
        ('ulonglong', np.ulonglong),
        ('int8', np.int8),
        ('int16', np.int16),
        ('int32', np.int32),
        ('int64', np.int64),
        ('uint8', np.uint8),
        ('uint16', np.uint16),
        ('uint32', np.uint32),
        ('uint64', np.uint64)
    ]
)
def test_integer_mapping(type_str: Text, real_type: Type):
    f = Feature(name='', order=0, type=type_str)
    assert f.get_type() == real_type
    assert np.issubdtype(f.get_type(), np.integer)


@pytest.mark.parametrize(
    'type_str, real_type',
    [
        ('float', float),  # native python float
        ('half', np.half),
        ('float16', np.float16),
        ('single', np.single),
        ('double', np.double),
        ('longdouble', np.longdouble),
        ('float32', np.float32),
        ('float64', np.float64),
        ('float_', np.float_)
    ]
)
def test_floating_point_mapping(type_str: Text, real_type: Type):
    f = Feature(name='', order=0, type=type_str)
    assert f.get_type() == real_type
    assert np.issubdtype(f.get_type(), np.floating)


@pytest.mark.parametrize(
    'type_str, real_type',
    [
        ('bool', bool),  # native python bool
        ('bool_', np.bool_),
    ]
)
def test_boolean_mapping(type_str: Text, real_type: Type):
    f = Feature(name='', order=0, type=type_str)
    assert f.get_type() == real_type
    assert np.issubdtype(f.get_type(), np.bool_)


@pytest.mark.parametrize(
    'type_str, real_type',
    [
        ('str', str),  # native python bool
        ('string_', np.string_),
        ('unicode_', np.unicode_)
    ]
)
def test_string_mapping(type_str: Text, real_type: Type):
    f = Feature(name='', order=0, type=type_str)
    assert f.get_type() == real_type
    assert np.issubdtype(f.get_type(), np.character)


def test_not_existing_type():
    with pytest.raises(ValueError):
        Feature(name='', order=0, type='unknown')


def test_not_valid_predict_proba():
    with pytest.raises(ValueError):
        Prediction(
            prediction='error',
            probabilities=[
                Probability(class_name=f'n{i}', class_index=i, value=val) for i, val in enumerate(
                    np.random.dirichlet(np.ones(10), size=1)[0] / 2)
            ]
        )


def test_valid_predict_proba():
    Prediction(
        prediction='good',
        probabilities=[
            Probability(class_name=f'n{i}', class_index=i, value=val) for i, val in enumerate(
                np.random.dirichlet(np.ones(10), size=1)[0])
        ]
    )
