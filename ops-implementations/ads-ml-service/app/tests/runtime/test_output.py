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


import typing

import numpy as np
import pandas as pd
import pytest

import app.runtime.output as app_runtime_output

EXPECTED = [
    ([0.5], 0.5),
    ([[0.5]], 0.5),
    ([0.5, 0.5], [0.5, 0.5]),
    ([[0.5, 0.5]], [0.5, 0.5]),
    ([[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]]),
    ([0.5], 0.5),
    ([[10]], 10),
    ([10, 10], [10, 10]),
    ([[10, 10]], [10, 10]),
    ([[10, 10], [10, 10]], [[10, 10], [10, 10]]),
    ([True], True),
    ([[True]], True),
    ([True, True], [True, True]),
    ([[True, True]], [True, True]),
    ([[True, True], [True, True]], [[True, True], [True, True]]),
    (['A'], 'A'),
    ([['A']], 'A'),
    (['A', 'A'], ['A', 'A']),
    ([['A', 'A']], ['A', 'A']),
    ([['A', 'A'], ['A', 'A']], [['A', 'A'], ['A', 'A']]),
]


@pytest.mark.parametrize(
    ('prediction_output', 'expected_output'),
    EXPECTED
)
def test_from_list(prediction_output, expected_output):
    assert app_runtime_output.from_list(prediction_output) == expected_output


@pytest.mark.parametrize(
    ('prediction_output', 'expected_output'),
    EXPECTED
)
def test_from_ndarray(prediction_output, expected_output):
    ndarray_output = np.array(prediction_output)
    assert app_runtime_output.from_ndarray(ndarray_output) == expected_output


@pytest.mark.parametrize(
    ('prediction_output', 'expected_output'),
    [
        # Single
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}], {'x': 0.5, 'y': 0.5}),
        # Multiple
        ([
             [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.3}],
             [{'name': 'x', 'value': -0.1}, {'name': 'y', 'value': 0.2}]
         ], [{'x': 0.5, 'y': 0.3}, {'x': -0.1, 'y': 0.2}]),
    ]
)
def test_from_ndarray(prediction_output, expected_output):
    if isinstance(prediction_output[0], typing.List):
        names = [feature['name'] for feature in prediction_output[0]]
        data = [[feature['value'] for feature in row] for row in prediction_output]
        dataframe_output = pd.DataFrame(data, columns=names)
    else:
        names = [feature['name'] for feature in prediction_output]
        data = [[feature['value'] for feature in prediction_output]]
        dataframe_output = pd.DataFrame(data, columns=names)
    assert app_runtime_output.from_dataframe(dataframe_output) == expected_output
