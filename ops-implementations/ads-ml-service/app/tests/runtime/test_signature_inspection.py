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
import pickle

import app.runtime.inspection as app_signature_inspection
import app.tests.predictors.pmml_sample.model as app_test_pmml


def test_pmml_input_schema_inspection(
        tmp_path: pathlib.Path
):
    pmml_path = app_test_pmml.get_pmml_file()
    with pmml_path.open(mode='rb') as fd:
        pmml_file = fd.read()
    input_schema = app_signature_inspection.inspect_pmml_input(pmml_file)

    assert input_schema == {
        'creditScore': 'double',
        'income': 'double',
        'loanAmount': 'double',
        'monthDuration': 'double',
        'rate': 'double',
        'yearlyReimbursement': 'double'
    }


def test_pmml_output_schema_inspection(
        tmp_path: pathlib.Path
):
    pmml_path = app_test_pmml.get_pmml_file()
    with pmml_path.open(mode='rb') as fd:
        pmml_file = fd.read()
    output_schema = app_signature_inspection.inspect_pmml_output(pmml_file)

    assert output_schema == {
        'probability_0': 'double',
        'probability_1': 'double',
        'predicted_paymentDefault': 'integer'
    }


def test_inspect_pickle_version():
    # Arrange
    p0 = pickle.dumps('test_0', protocol=0)
    p1 = pickle.dumps('test_1', protocol=1)
    p2 = pickle.dumps('test_2', protocol=2)
    p3 = pickle.dumps(str.encode('test_3'), protocol=3)
    p4 = pickle.dumps('test_4', protocol=4)

    # When
    ver_0 = app_signature_inspection.inspect_pickle_version(p0)
    ver_1 = app_signature_inspection.inspect_pickle_version(p1)
    ver_2 = app_signature_inspection.inspect_pickle_version(p2)
    ver_3 = app_signature_inspection.inspect_pickle_version(p3)
    ver_4 = app_signature_inspection.inspect_pickle_version(p4)

    # Assert
    assert ver_0 == 0
    assert ver_1 == 1
    assert ver_2 == 2
    assert ver_3 == 3
    assert ver_4 == 4


def test_inspect_pmml_subtype():
    # When
    sub_type_regression = app_signature_inspection.inspect_pmml_subtype(
        str.encode(app_test_pmml.get_pmml_file().read_text()))
    sub_type_scorecard = app_signature_inspection.inspect_pmml_subtype(
        str.encode(app_test_pmml.get_pmml_scorecard_file().read_text()))

    # Assert
    assert sub_type_regression == 'RegressionModel'
    assert sub_type_scorecard == 'Scorecard'
