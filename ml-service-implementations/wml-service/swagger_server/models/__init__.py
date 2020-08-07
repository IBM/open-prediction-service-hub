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
# coding: utf-8

# flake8: noqa
from __future__ import absolute_import
# import models into model package
from swagger_server.models.all_of_machine_learning_model_output_schema import AllOfMachineLearningModelOutputSchema
from swagger_server.models.capabilities import Capabilities
from swagger_server.models.error import Error
from swagger_server.models.feature import Feature
from swagger_server.models.link import Link
from swagger_server.models.machine_learning_model import MachineLearningModel
from swagger_server.models.machine_learning_model_endpoint import MachineLearningModelEndpoint
from swagger_server.models.machine_learning_model_endpoints import MachineLearningModelEndpoints
from swagger_server.models.machine_learning_models import MachineLearningModels
from swagger_server.models.output_schema import OutputSchema
from swagger_server.models.parameter import Parameter
from swagger_server.models.prediction import Prediction
from swagger_server.models.prediction_response import PredictionResponse
from swagger_server.models.server_status import ServerStatus
