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

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.endpoints import Endpoints  # noqa: E501
from openapi_server.models.models import Models  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDiscoverController(BaseTestCase):
    """DiscoverController integration test stubs"""

    def test_get_endpoint_by_id(self):
        """Test case for get_endpoint_by_id

        Get an Endpoint
        """
        response = self.client.open(
            '/endpoints/{endpoint_id}'.format(endpoint_id='endpoint_id_example'),
            method='GET')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        endpoint = Endpoint.from_dict(response_dict_decode)
        assert (
                endpoint is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_model_by_id(self):
        """Test case for get_model_by_id

        Get a Model
        """
        response = self.client.open(
            '/models/{model_id}'.format(model_id='model_id_example'),
            method='GET')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        model = Model.from_dict(response_dict_decode)
        assert (
                model is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

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
        endpoints = Endpoints.from_dict(response_dict_decode)
        assert (
                endpoints.endpoints is not None
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
        machine_learning_models = Models.from_dict(response_dict_decode)
        assert (
                machine_learning_models.models is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
