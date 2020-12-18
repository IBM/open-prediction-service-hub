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


import pickle
import typing

import pytest

import app.runtime.input as app_runtime_input
import app.runtime.wrapper as app_runtime_wrapper
import app.schemas.binary_config as app_binary_config
import app.schemas.impl as app_schemas_impl
import app.tests.predictors.identity.model as app_test_identity
import app.tests.predictors.pmml.model as app_test_pmml
import app.tests.predictors.xgboost.model as app_test_xgboost

INPUT = [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}]


@pytest.mark.parametrize(
    ('prediction_input', 'model', 'input_type', 'output_type', 'binary_format', 'input_handler'),
    [
        (
                INPUT,
                pickle.dumps(app_test_identity.get_identity_predictor()),
                app_binary_config.ModelInput.LIST,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.PICKLE,
                app_runtime_input.to_list
        ),
        (
                INPUT,
                pickle.dumps(app_test_identity.get_identity_predictor()),
                app_binary_config.ModelInput.NUMPY_ARRAY,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.PICKLE,
                app_runtime_input.to_ndarray
        ),
        (
                INPUT,
                pickle.dumps(app_test_identity.get_identity_predictor()),
                app_binary_config.ModelInput.DATAFRAME,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.PICKLE,
                app_runtime_input.to_dataframe
        ),
        (
                INPUT,
                pickle.dumps(app_test_identity.get_identity_predictor()),
                app_binary_config.ModelInput.DMATRIX,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.PICKLE,
                app_runtime_input.to_dmatrix
        ),
        (
                INPUT,
                pickle.dumps(app_test_identity.get_identity_predictor()),
                app_binary_config.ModelInput.AUTO,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.PICKLE,
                app_runtime_input.to_dataframe
        ),
        (
                INPUT,
                app_test_xgboost.get_xgboost_classification_predictor(),
                app_binary_config.ModelInput.AUTO,
                app_binary_config.ModelOutput.NUMPY_ARRAY,
                app_binary_config.ModelWrapper.BST,
                app_runtime_input.to_dmatrix
        ),
        (
                INPUT,
                app_test_pmml.get_pmml_file,
                app_binary_config.ModelInput.AUTO,
                app_binary_config.ModelOutput.DATAFRAME,
                app_binary_config.ModelWrapper.PMML,
                app_runtime_input.to_dataframe
        ),
    ]
)
def test_model_invocation_executor_input_handling(
        prediction_input: typing.List[typing.Any],
        model: typing.Any,
        input_type: app_binary_config.ModelInput,
        output_type: app_binary_config.ModelOutput,
        binary_format: app_binary_config.ModelWrapper,
        input_handler: typing.Callable,
        tmp_path
):
    input_params = [app_schemas_impl.ParameterImpl(**param) for param in prediction_input]
    if binary_format is app_binary_config.ModelWrapper.BST:
        model_path = tmp_path.joinpath('model.bst')
        model.save_model(fname=model_path.__str__())
        with model_path.open(mode='rb') as fd:
            content = fd.read()
        model_invocation_executor = app_runtime_wrapper.ModelInvocationExecutor(
            model=content,
            input_type=input_type,
            output_type=output_type,
            binary_format=binary_format
        )
    elif binary_format is app_binary_config.ModelWrapper.PMML:
        pmml_path = app_test_pmml.get_pmml_file(tmp_path)
        with pmml_path.open(mode='rb') as fd:
            pmml_file = fd.read()
        model_invocation_executor = app_runtime_wrapper.ModelInvocationExecutor(
            model=pmml_file,
            input_type=input_type,
            output_type=output_type,
            binary_format=binary_format
        )
    else:
        model_invocation_executor = app_runtime_wrapper.ModelInvocationExecutor(
            model=model,
            input_type=input_type,
            output_type=output_type,
            binary_format=binary_format
        )
    model_invocation_executor.input_handling(input_params)

    assert model_invocation_executor.input_handler == input_handler
