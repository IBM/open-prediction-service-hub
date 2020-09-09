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


import sklearnserver
import xgbserver
import xgboost


class InMemoryKFModel(object):
    def __init__(self, predictor_binary: typ.Any):
        self.binary = predictor_binary


class SKLearnModelImpl(InMemoryKFModel, sklearnserver.SKLearnModel):
    def __init__(self, predictor_binary: object):
        InMemoryKFModel.__init__(self, predictor_binary=predictor_binary)
        sklearnserver.SKLearnModel.__init__(self, name='', model_dir='')

    def load(self):
        setattr(self, '_model', self.binary)
        self.ready = True


class XGBoostModelImpl(InMemoryKFModel, xgbserver.XGBoostModel):
    def __init__(self, predictor_binary: object):
        InMemoryKFModel.__init__(self, predictor_binary=predictor_binary)
        xgbserver.XGBoostModel.__init__(self, name='', model_dir='', nthread=16)

    def load(self):
        setattr(self, '_booster', xgboost.Booster(params={"nthread": self.nthread}, model_file=self.binary))
        self.ready = True
