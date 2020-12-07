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


import numpy as np
import pandas as pd
import sklearn.ensemble as skl_ensemble

import app.tests.utils.utils as app_utils


def get_classification_predictor() -> skl_ensemble.RandomForestClassifier:
    classifier = skl_ensemble.RandomForestClassifier(random_state=42)
    x_random = pd.DataFrame(data=np.random.rand(10, 2), columns=['x', 'y'])
    y_random = np.array([app_utils.random_string() for _ in range(10)])
    classifier.fit(x_random, y_random)
    return classifier
