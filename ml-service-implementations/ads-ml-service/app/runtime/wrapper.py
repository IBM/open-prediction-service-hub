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


from __future__ import annotations

import io
import logging
import typing as typ

import joblib

try:
    import pypmml
except ImportError:
    pypmml = None

try:
    import xgboost as xgb
except ImportError:
    xgb = None

import app.runtime.input as app_input
import app.runtime.output as app_output
import app.schemas.binary_config as app_binary_config

LOGGER = logging.getLogger(__name__)


class InMemoryModel:
    def __init__(self, model: typ.Any):
        self.model = model

    def has_method(self, method_name: typ.Text):
        return hasattr(self.model, method_name)

    def predict(self, request: typ.Any) -> typ.Any:
        try:
            return self.model.predict(request)
        except Exception:
            LOGGER.exception('Failed to predict %s', request)
            raise

    def predict_proba(self, request: typ.Any) -> typ.Any:
        if not hasattr(self.model, 'predict_proba'):
            return None
        try:
            return self.model.predict_proba(request)
        except Exception:
            LOGGER.exception('Failed to predict %s', request)
            raise


class JoblibFormat(InMemoryModel):
    @staticmethod
    def load(binary: typ.Any) -> JoblibFormat:
        model = joblib.load(io.BytesIO(binary))
        return JoblibFormat(model)


class PMMLFormat(InMemoryModel):
    @staticmethod
    def load(binary: typ.Any) -> PMMLFormat:
        if not pypmml:
            LOGGER.exception('pypmml is not installed')
            raise RuntimeError('pypmml is not installed')
        model = pypmml.Model.load(io.BytesIO(binary))
        return PMMLFormat(model)


class SBTFormat(InMemoryModel):
    @staticmethod
    def load(binary: typ.Any) -> SBTFormat:
        if not pypmml:
            LOGGER.exception('xgboost is not installed')
            raise RuntimeError('xgboost is not installed')
        model = xgb.Booster(params={"nthread": 4}, model_file=bytearray(binary))
        return SBTFormat(model)


WRAPPERS = {
    app_binary_config.ModelWrapper.JOBLIB: JoblibFormat,
    app_binary_config.ModelWrapper.PMML: PMMLFormat,
    app_binary_config.ModelWrapper.BST: SBTFormat
}


class ModelInvocationExecutor:
    def __init__(
            self,
            *,
            model: typ.Any,
            input_type: app_binary_config.ModelInput = app_binary_config.ModelInput.DATAFRAME,
            output_type: app_binary_config.ModelOutput = app_binary_config.ModelOutput.NUMPY_ARRAY,
            binary_format: app_binary_config.ModelWrapper = app_binary_config.ModelWrapper.JOBLIB
    ):
        self.input_handler = app_input.INPUT_HANDLING[input_type]
        self.output_handler = app_output.OUTPUT_HANDLING[output_type]
        self.model_wrapper = WRAPPERS[binary_format]

        self.loaded_model = self.model_wrapper.load(model)
        self.can_predict_proba = self.loaded_model.has_method('predict_proba')

    def predict(self, request: typ.Any) -> typ.Any:
        prepared_data = self.input_handler(request)
        LOGGER.debug('ML input: %s', prepared_data)

        predict = self.loaded_model.predict(prepared_data)
        LOGGER.debug('ML output: %s', predict)
        formatted_predict = self.output_handler(predict)
        if not self.can_predict_proba:
            return {'result': {'predictions': formatted_predict}}
        else:
            predict_proba = self.loaded_model.predict_proba(prepared_data)
            LOGGER.debug('ML output(scores): %s', predict_proba)
            formatted_predict_proba = self.output_handler(predict_proba)
            return {'result': {'predictions': formatted_predict, 'scores': formatted_predict_proba}}
