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

from typing import Text, List, Dict, Optional, Union

import numpy as np
from pydantic import BaseModel, Field, validator


class ServerStatus(BaseModel):
    model_count: np.long = Field(..., description='Number of ml models in local provider')


class Probability(BaseModel):
    class_name: Optional[Text]
    class_index: int
    value: np.float64


class Prediction(BaseModel):
    """Ml output for model.predict(array_like) and model.predict_proba(array_like)"""
    prediction: Text = Field(..., description='Model output for Classification/Regression')
    probabilities: Optional[List[Probability]] = Field(None, description='Probabilities for classification result')

    @validator('probabilities', always=True)
    def probabilities_check(cls, probabilities: Optional[List[Probability]]) -> Optional[List[Probability]]:
        if probabilities is None:
            return probabilities
        if np.isclose(sum([pair.value for pair in probabilities]), 1, rtol=1e-05, atol=1e-05, equal_nan=False):
            return probabilities
        else:
            raise ValueError('The sum of probabilities needs to be 1')
