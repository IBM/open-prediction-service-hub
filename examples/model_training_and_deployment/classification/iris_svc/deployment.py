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


import json
import pickle
from pathlib import Path


def iris_archive():
    with Path(__file__).resolve().parent.joinpath('iris.json').open(mode='r') as fd:
        conf = json.load(fd)
    with Path(__file__).resolve().parent.joinpath('iris-model.pkl').open(mode='rb') as fd:
        estimator = pickle.load(
            file=fd
        )
    with Path(__file__).resolve().parent.joinpath('iris-archive.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj={
                'model': estimator,
                'model_config': conf
            },
            file=fd
        )


if __name__ == '__main__':
    iris_archive()

