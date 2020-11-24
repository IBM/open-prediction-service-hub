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


import pathlib
import typing

import numpy as np
import xgboost
import yaml

from app.tests.utils import utils as app_utils


def get_conf() -> typing.Dict[typing.Text, typing.Any]:
    with pathlib.Path(__file__).resolve().parent.joinpath('deployment_config.yaml').open(mode='r') as fd:
        return yaml.safe_load(fd)


def get_xgboost_classification_predictor() -> xgboost.XGBClassifier:
    classifier = xgboost.XGBClassifier(random_state=42)
    x_random = np.random.rand(10, 2)
    y_random = np.array([app_utils.random_string() for _ in range(10)])
    classifier.fit(x_random, y_random)
    return classifier
