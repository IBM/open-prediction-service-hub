# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.capabilities import Capabilities  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.server_info import ServerInfo  # noqa: E501
from openapi_server.test import BaseTestCase


class TestInfoController(BaseTestCase):
    """InfoController integration test stubs"""

    def test_get_capabilities(self):
        """Test case for get_capabilities

        Get Server Capabilities
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/capabilities',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_info(self):
        """Test case for get_info

        Get Server Information and Status
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/info',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
