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

import yaml
from sklearn.base import BaseEstimator


class IdentityPredictor(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, x, y) -> typing.NoReturn:
        pass

    def predict(self, x) -> typing.Any:
        return x


def get_conf() -> typing.Dict[typing.Text, typing.Any]:
    with pathlib.Path(__file__).resolve().parent.joinpath('deployment_config.yaml').open(mode='r') as fd:
        return yaml.safe_load(fd)


def get_identity_predictor() -> IdentityPredictor:
    return IdentityPredictor()
