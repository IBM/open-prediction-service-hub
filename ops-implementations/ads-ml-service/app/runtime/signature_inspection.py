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


import io
import logging
import typing

import pypmml
import pypmml.base as pypmml_base


LOGGER = logging.getLogger(__name__)


def load_pmml_model(model_file: bytes) -> pypmml.Model:
    try:
        model = pypmml.Model.load(io.BytesIO(model_file))
    except pypmml_base.PmmlError:
        LOGGER.exception('Can not load pmml model')
        raise ValueError('Can not load pmml model')
    return model


def inspect_pmml_input(model_file: bytes) -> typing.Optional[typing.Dict[str, str]]:
    model = load_pmml_model(model_file)

    if model.inputFields is not None and len(model.inputFields) > 0:
        return {field.name: field.dataType for field in model.inputFields}
    else:
        return None


def inspect_pmml_output(model_file: bytes) -> typing.Optional[typing.Dict[str, str]]:
    model = load_pmml_model(model_file)

    if model.outputFields is not None and len(model.outputFields) > 0:
        return {field.name: field.dataType for field in model.outputFields}
    else:
        return None
