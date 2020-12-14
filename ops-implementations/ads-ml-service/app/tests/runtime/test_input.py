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

import pytest

import app.runtime.input as app_runtime_input
import app.schemas.impl as app_schemas_impl

HETEROGENEOUS = [
    # Single
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}], [[0.5, 0.5]]),
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 10}], [[0.5, 10]]),
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': True}], [[0.5, True]]),
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 'good'}], [[0.5, 'good']]),
    ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': 10}], [[10, 10]]),
    ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': True}], [[10, True]]),
    ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': 'good'}], [[10, 'good']]),
    ([{'name': 'x', 'value': True}, {'name': 'y', 'value': True}], [[True, True]]),
    ([{'name': 'x', 'value': True}, {'name': 'y', 'value': 'good'}], [[True, 'good']]),
    ([{'name': 'x', 'value': 'bad'}, {'name': 'y', 'value': 'good'}], [['bad', 'good']]),
    # Multiple
    ([
         [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 'bad'}],
         [{'name': 'x', 'value': -0.1}, {'name': 'y', 'value': 'good'}]
     ], [[0.5, 'bad'], [-0.1, 'good']]),
]

HOMOGENEOUS = [
    # Single
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}], [[0.5, 0.5]]),
    ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 10}], [[0.5, 10]]),
    ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': 10}], [[10, 10]]),
    ([{'name': 'x', 'value': True}, {'name': 'y', 'value': True}], [[True, True]]),
    ([{'name': 'x', 'value': 'bad'}, {'name': 'y', 'value': 'good'}], [['bad', 'good']]),
    # Multiple
    ([
         [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.3}],
         [{'name': 'x', 'value': -0.1}, {'name': 'y', 'value': 0.2}]
     ], [[0.5, 0.3], [-0.1, 0.2]]),
]


@pytest.mark.parametrize(
    ('prediction_input', 'expected_output'),
    HETEROGENEOUS
)
def test_to_list(prediction_input, expected_output):
    if isinstance(prediction_input[0], typing.List):
        input_params = [[app_schemas_impl.ParameterImpl(**param) for param in row] for row in prediction_input]
    else:
        input_params = [app_schemas_impl.ParameterImpl(**param) for param in prediction_input]

    assert app_runtime_input.to_list(input_params) == expected_output


@pytest.mark.parametrize(
    ('prediction_input', 'expected_output'),
    HOMOGENEOUS
)
def test_to_ndarray(prediction_input, expected_output):
    if isinstance(prediction_input[0], typing.List):
        input_params = [[app_schemas_impl.ParameterImpl(**param) for param in row] for row in prediction_input]
    else:
        input_params = [app_schemas_impl.ParameterImpl(**param) for param in prediction_input]

    assert app_runtime_input.to_ndarray(input_params).tolist() == expected_output


@pytest.mark.parametrize(
    ('prediction_input', 'expected_output'),
    HETEROGENEOUS
)
def test_to_dataframe(prediction_input, expected_output):
    if isinstance(prediction_input[0], typing.List):
        names = [feature['name'] for feature in prediction_input[0]]
        input_params = [[app_schemas_impl.ParameterImpl(**param) for param in row] for row in prediction_input]
    else:
        names = [feature['name'] for feature in prediction_input]
        input_params = [app_schemas_impl.ParameterImpl(**param) for param in prediction_input]
    df = app_runtime_input.to_dataframe(input_params)

    assert df.columns.tolist() == names
    assert df.values.tolist() == expected_output
