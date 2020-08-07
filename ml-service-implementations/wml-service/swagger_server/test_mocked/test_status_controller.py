# coding: utf-8

from __future__ import absolute_import

from unittest import mock

from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.capability import Capability  # noqa: E501
from swagger_server.models.server_status import ServerStatus  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.controllers.status_controller import get_capabilities, get_status


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    # GET CAPABILITIES
    def test_get_capabilities(self):
        """Test case for get_capabilities

        Get Server Capabilities
        """
        expected = "{'capabilities': ['" + Capability.STATUS + "', '" + Capability.DISCOVER + "', '" + Capability.RUNTIME + "']}"
        response = get_capabilities()

        assert isinstance(response, Capabilities)
        assert str(response) == expected, 'response is not matching expected response'

    # GET STATUS
    @mock.patch("swagger_server.controllers.status_controller.boto3.client")
    def test_get_status(self, mock_boto_client):
        """Test case for get_status

        Get Server Status
        """
        expected = "{'error': None, 'status': 'ok'}"
        response = get_status()

        assert isinstance(response, ServerStatus)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')

    @mock.patch("swagger_server.controllers.status_controller.boto3.client")
    def test_get_status_error(self, mock_boto_client):
        """Test case for get_status

        Get Server Status
        """
        mock_boto_client.side_effect = KeyError('foo')

        expected = "{\'error\': \"<class \'KeyError\'>\", \'status\': \'error\'}"
        response = get_status()

        assert isinstance(response, ServerStatus)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')


if __name__ == '__main__':
    import unittest
    unittest.main()
