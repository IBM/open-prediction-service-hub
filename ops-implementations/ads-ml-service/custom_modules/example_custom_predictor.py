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
from typing import NoReturn

import sklearn.base as skl_base
import sklearn.utils as skl_utils
import sklearn.utils.validation as skl_validation


class IdentityPredictor(skl_base.BaseEstimator, skl_base.ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, x, y) -> NoReturn:
        setattr(self, 'fitted_', True)

    def predict(self, x) -> typing.Any:
        """
        x is an array-like object
        """
        skl_validation.check_is_fitted(self, attributes=['fitted_'])
        x_checked = skl_utils.check_array(x)
        return x_checked
