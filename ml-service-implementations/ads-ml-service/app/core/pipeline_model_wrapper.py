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


import app.core.kfserving_impl as kfserving_impl
import pandas as pd
import numpy as np
import typing as typ


class DataframeModel(kfserving_impl.InMemoryKFModel):
    def predict(self, request: typ.Dict[typ.Text, pd.DataFrame]) -> typ.Dict:
        instances = request['instances']
        try:
            model_output = self.binary.predict(instances)
        except Exception as e:
            raise Exception(f'Failed to predict {e}')
        if isinstance(model_output, pd.DataFrame):
            result = model_output.to_dict(orient='records')
        elif isinstance(model_output, np.ndarray):
            result = model_output.tolist()
        else:
            result = str(model_output)
        return {'predictions': result}
