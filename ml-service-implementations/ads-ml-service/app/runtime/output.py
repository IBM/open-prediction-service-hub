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

import app.schemas.binary_config as app_binary_config


def from_list(
        output: typing.List[typing.Any]
) -> typing.Any:
    if not isinstance(output[0], typing.List):
        # A 1-dimensional list
        if len(output) == 1:
            # Singleton list
            return output[0]
        else:
            return output
    else:
        # A N-dimensional list
        if len(output) == 1:
            # Singleton list
            if len(output[0]) == 1:
                # Row element is not array
                return output[0][0]
            else:
                # Row element is array
                return output[0]
        else:
            return output


def from_ndarray(
        output: np.ndarray
) -> typing.Any:
    return from_list(output.tolist())


def from_dataframe(
        output: pd.DataFrame
) -> typing.Any:
    return from_list(output.to_dict(orient='records'))


OUTPUT_HANDLING = {
    app_binary_config.ModelOutput.LIST: from_list,
    app_binary_config.ModelOutput.NUMPY_ARRAY: from_ndarray,
    app_binary_config.ModelOutput.DATAFRAME: from_dataframe
}
