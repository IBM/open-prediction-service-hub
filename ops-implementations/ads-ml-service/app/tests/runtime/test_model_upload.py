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


import app.runtime.model_upload as app_model_upload
import app.schemas.binary_config as app_binary_config
import app.tests.predictors.pmml_sample.model as app_test_pmml


def test_infer_binary_file_format():
    inferred_1 = app_model_upload.infer_file_format(
        b'',
        '.PKL'
    )
    inferred_2 = app_model_upload.infer_file_format(
        b'',
        '.Joblib'
    )
    inferred_3 = app_model_upload.infer_file_format(
        b'',
        '.Pickle'
    )

    assert inferred_1 == app_binary_config.ModelWrapper.PICKLE
    assert inferred_2 == app_binary_config.ModelWrapper.JOBLIB
    assert inferred_3 == app_binary_config.ModelWrapper.PICKLE


def test_infer_text_file_format():
    with app_test_pmml.get_pmml_file().open(mode='rb') as fd:
        model = fd.read()
    inferred_1 = app_model_upload.infer_file_format(
        model,
        '.xml'
    )
    inferred_2 = app_model_upload.infer_file_format(
        b'<PMML EOF',
        '.xml'
    )
    assert inferred_1 == app_binary_config.ModelWrapper.PMML
    assert inferred_2 is None
