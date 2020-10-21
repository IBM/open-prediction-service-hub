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


import pytest
import typing
import numpy as np

import predictions.schemas.prediction as prediction
import predictions.core.util as util


@pytest.mark.parametrize(
    'type_str',
    [
        'int',
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

        'float',
        'half',
        'float16',
        'single',
        'double',
        'longdouble',
        'float32',
        'float64',
        'float_',

        'bool',
        'bool_',

        'str',
        # 'string_',  # python 2 zero-terminated bytes is not needed
        'unicode_'
    ]
)
def test_output_data_mapping(type_str: typing.Text):
    typ = getattr(np, type_str)
    instance = typ(3)
    instance_str = util.data_to_str(instance)

    p = prediction.Prediction(prediction=instance_str)
    reverse = typ(p.prediction)
    assert reverse == instance
