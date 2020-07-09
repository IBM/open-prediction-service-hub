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


import random
from typing import NoReturn

import numpy as np
import pytest
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


@pytest.fixture
def regression_predictor():
    class DummyRegressor(BaseEstimator, RegressorMixin):
        def __init__(self):
            pass

        def fit(self, x, y) -> NoReturn:
            x_, y_ = check_X_y(x, y)
            setattr(self, 'range', (min(y_), max(y_)))

        def predict(self, x) -> np.ndarray:
            """
            data is an array-like object
            """
            check_is_fitted(self)
            check_array(x)
            r = getattr(self, 'range')
            return np.array([random.uniform(a=r[0], b=r[1]) for _ in range(len(x))])

    return DummyRegressor()


@pytest.fixture
def classification_predictor():
    class DummyClassifier(BaseEstimator, ClassifierMixin):
        def __init__(self):
            pass

        def fit(self, x, y) -> NoReturn:
            x_, y_ = check_X_y(x, y)
            setattr(self, 'unique', np.unique(y_))

        def predict(self, x) -> np.ndarray:
            """
            data is an array-like object
            """
            check_is_fitted(self)
            check_array(x)
            u = getattr(self, 'unique')
            return np.array([random.choice(u) for _ in range(len(x))])

    return DummyClassifier()


@pytest.fixture
def classification_with_prob_predictor():
    class DummyClassifier(BaseEstimator, ClassifierMixin):
        def __init__(self):
            pass

        def fit(self, x, y) -> NoReturn:
            x_, y_ = check_X_y(x, y)
            setattr(self, 'unique', np.unique(y_))

        def predict(self, x) -> np.ndarray:
            """
            data is an array-like object
            """
            check_is_fitted(self)
            check_array(x)
            u = getattr(self, 'unique')
            return np.array([np.random.dirichlet(np.ones(len(u)), size=1)[0] for _ in range(len(x))])

    return DummyClassifier()
