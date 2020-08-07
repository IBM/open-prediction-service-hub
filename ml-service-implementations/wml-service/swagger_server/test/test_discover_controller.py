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

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.machine_learning_model_endpoints import MachineLearningModelEndpoints  # noqa: E501
from swagger_server.models.machine_learning_models import MachineLearningModels  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDiscoverController(BaseTestCase):
    """DiscoverController integration test stubs"""

    def test_list_endpoints(self):
        """Test case for list_endpoints

        List Endpoints
        """
        query_string = [('model_id', 'model_id_example')]
        response = self.client.open(
            '/endpoints',
            method='GET',
            query_string=query_string)
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        machine_learning_model_endpoints = MachineLearningModelEndpoints.from_dict(response_dict_decode)
        assert (
                machine_learning_model_endpoints.endpoints is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_models(self):
        """Test case for list_models

        List Models
        """
        response = self.client.open(
            '/models',
            method='GET')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        machine_learning_models = MachineLearningModels.from_dict(response_dict_decode)
        assert (
                machine_learning_models.models is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
