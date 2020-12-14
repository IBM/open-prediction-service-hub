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

import nyoka
import sklearn.pipeline as skl_pipeline
import yaml

import app.tests.predictors.scikit_learn.model


def get_pmml_file(tmp: pathlib.Path) -> pathlib.Path:
    if not tmp.is_dir():
        raise ValueError(f'{tmp} is not directory')
    predictor = app.tests.predictors.scikit_learn.model.get_classification_predictor()
    dest = tmp.joinpath('model.pmml')
    nyoka.skl_to_pmml(
        pipeline=skl_pipeline.Pipeline([("model", predictor)]),
        col_names=predictor.classes_.tolist(),
        pmml_f_name=dest
    )
    return dest


def get_conf() -> typing.Dict[typing.Text, typing.Any]:
    with pathlib.Path(__file__).resolve().parent.joinpath('deployment_config.yaml').open(mode='r') as fd:
        return yaml.safe_load(fd)
