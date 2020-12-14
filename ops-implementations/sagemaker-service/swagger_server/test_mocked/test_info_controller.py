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

from unittest import mock

from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.capability import Capability  # noqa: E501
from swagger_server.models.server_info import ServerInfo  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.controllers.info_controller import get_capabilities, get_info


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    # GET CAPABILITIES
    def test_get_capabilities(self):
        """Test case for get_capabilities

        Get Server Capabilities
        """
        expected = "{'capabilities': ['" + Capability.INFO + "', '" + Capability.DISCOVER + "', '" + Capability.RUN + "']}"
        response = get_capabilities()

        assert isinstance(response, Capabilities)
        assert str(response) == expected, 'response is not matching expected response'

    # GET STATUS
    @mock.patch("swagger_server.controllers.info_controller.boto3.client")
    def test_get_info(self, mock_boto_client):
        """Test case for get_info

        Get Server Status
        """
        expected = "{'error': None,\n" +\
                   " 'info': {'description': 'Open Prediction Service for Amazon Sagemaker based '\n" + \
                   "                         'on OPSv2 API'},\n" + \
                   " 'status': 'ok'}"
        response = get_info()

        assert isinstance(response, ServerInfo)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')

    @mock.patch("swagger_server.controllers.info_controller.boto3.client")
    def test_get_info_error(self, mock_boto_client):
        """Test case for get_info

        Get Server Status
        """
        mock_boto_client.side_effect = KeyError('foo')

        expected = '{\'error\': "<class \'KeyError\'>",\n' + \
                   ' \'info\': {\'description\': \'Open Prediction Service for Amazon Sagemaker based \'\n' + \
                   '                         \'on OPSv2 API\'},\n' + \
                   ' \'status\': \'error\'}'
        response = get_info()

        assert isinstance(response, ServerInfo)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')


if __name__ == '__main__':
    import unittest
    unittest.main()
