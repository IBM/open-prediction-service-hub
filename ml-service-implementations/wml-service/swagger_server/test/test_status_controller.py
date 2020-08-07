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

from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.server_status import ServerStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    def test_get_capabilities(self):
        """Test case for get_capabilities

        Get Server Capabilities
        """
        response = self.client.open(
            '/capabilities',
            method='GET')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        capabilities = Capabilities.from_dict(response_dict_decode)
        assert (
                capabilities.capabilities is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_status(self):
        """Test case for get_status

        Get Server Status
        """
        response = self.client.open(
            '/status',
            method='GET')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        server_status = ServerStatus.from_dict(response_dict_decode)
        assert server_status.status is not None
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
