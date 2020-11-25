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


import typing as typ

import numpy as np
import pandas as pd
import xgboost as xgb

import app.schemas.binary_config as app_binary_config
import app.schemas.impl as app_schema_impl


def to_list(
        input_: typ.Union[typ.List[typ.List[app_schema_impl.ParameterImpl]], typ.List[app_schema_impl.ParameterImpl]]
) -> typ.Union[typ.List[typ.List[typ.Any]], typ.List[typ.Any]]:
    if isinstance(input_[0], typ.List):
        return [[col.value for col in row] for row in input_]
    else:
        return [[col.value for col in input_]]


def to_ndarray(
        input_: typ.Union[typ.List[typ.List[app_schema_impl.ParameterImpl]], typ.List[app_schema_impl.ParameterImpl]]
) -> np.ndarray:
    return np.array(to_list(input_))


def to_dataframe(
        input_: typ.Union[typ.List[typ.List[app_schema_impl.ParameterImpl]], typ.List[app_schema_impl.ParameterImpl]]
) -> pd.DataFrame:
    if isinstance(input_[0], typ.List):
        return pd.DataFrame(to_list(input_), columns=[col.name for col in input_[0]])
    else:
        return pd.DataFrame(to_list(input_), columns=[col.name for col in input_])


def to_dmatrix(
        input_: typ.Union[typ.List[typ.List[app_schema_impl.ParameterImpl]], typ.List[app_schema_impl.ParameterImpl]]
) -> xgb.DMatrix:
    return xgb.DMatrix(to_ndarray(input_), nthread=4)


INPUT_HANDLING = {
    app_binary_config.ModelInput.LIST: to_list,
    app_binary_config.ModelInput.NUMPY_ARRAY: to_ndarray,
    app_binary_config.ModelInput.DATAFRAME: to_dataframe,
    app_binary_config.ModelInput.DMATRIX: to_dmatrix,
}
