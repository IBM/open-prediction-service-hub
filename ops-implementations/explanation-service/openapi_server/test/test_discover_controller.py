# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoints import Endpoints  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.models import Models  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDiscoverController(BaseTestCase):
    """DiscoverController integration test stubs"""

    def test_get_endpoint_by_id(self):
        """Test case for get_endpoint_by_id

        Get an Endpoint
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/endpoints/{endpoint_id}'.format(endpoint_id='endpoint_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_model_by_id(self):
        """Test case for get_model_by_id

        Get a Model
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/models/{model_id}'.format(model_id='model_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_endpoints(self):
        """Test case for list_endpoints

        List Endpoints
        """
        query_string = [('model_id', 'model_id_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/endpoints',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_models(self):
        """Test case for list_models

        List Models
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/models',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
