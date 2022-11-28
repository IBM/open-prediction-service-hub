#!/usr/bin/env python3
#
# Copyright 2021 IBM
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


import logging
import typing
import pickletools

import pypmml.base as pypmml_base

import app.runtime.wrapper as app_runtime_wrapper
import app.schemas.binary_config as app_binary_config

LOGGER = logging.getLogger(__name__)


def load_pmml_model(model_file: bytes) -> app_runtime_wrapper.ModelInvocationExecutor:
    try:
        runner = app_runtime_wrapper.ModelInvocationExecutor(
            model=model_file,
            input_type=app_binary_config.ModelInput.AUTO,
            output_type=app_binary_config.ModelOutput.AUTO,
            binary_format=app_binary_config.ModelWrapper.PMML
        )
    except pypmml_base.PmmlError:
        LOGGER.exception('Can not load pmml model')
        raise ValueError('Can not load pmml model')
    return runner


def inspect_pmml_input(model_file: bytes) -> typing.Optional[typing.Dict[str, str]]:
    wrapper = load_pmml_model(model_file).loaded_model

    if wrapper.model.inputFields is not None and len(wrapper.model.inputFields) > 0:
        return {field.name: field.dataType for field in wrapper.model.inputFields}
    else:
        return None


def inspect_pmml_output(model_file: bytes) -> typing.Optional[typing.Dict[str, str]]:
    wrapper = load_pmml_model(model_file).loaded_model

    if wrapper.model.outputFields is not None and len(wrapper.model.outputFields) > 0:
        return {field.name: field.dataType for field in wrapper.model.outputFields}
    else:
        return None


def inspect_pmml_model_name(model_file: bytes) -> typing.Optional[str]:
    wrapper = load_pmml_model(model_file).loaded_model

    if wrapper.model.modelName is not None:
        return wrapper.model.modelName
    else:
        return None


def inspect_pmml_subtype(model_file: bytes) -> typing.Optional[str]:
    wrapper = load_pmml_model(model_file).loaded_model
    return wrapper.model.modelElement


def inspect_pickle_version(model_file: bytes) -> int:
    return max(op[0].proto for op in pickletools.genops(model_file))
