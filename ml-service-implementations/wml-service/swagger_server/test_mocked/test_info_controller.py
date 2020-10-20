# coding: utf-8

from __future__ import absolute_import

from unittest import mock

from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.capability import Capability  # noqa: E501
from swagger_server.models.server_info import ServerInfo  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.controllers.info_controller import get_capabilities, get_info

from swagger_server.test_mocked.util import MOCKED_CREDENTIALS, mock_wml_credentials


class TestInfoController(BaseTestCase):
    """InfoController integration test stubs"""

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
    @mock_wml_credentials('info_controller')
    @mock.patch("swagger_server.controllers.info_controller.requests.request")
    def test_get_info(self, mock_request, mock_cred):
        """Test case for get_info

        Get Server Information and Status
        """
        mock_request.return_value.json.return_value = {
            "resources": [
                {
                    "entity": {
                        "asset": {
                            "id": "59dac523-e5e0-452b-aa04-50a144beced5"
                        },
                        "name": "Notebook import additional data",
                        "online": {
                            "parameters": {}
                        },
                        "status": {
                            "message": {
                                "text": ""
                            },
                            "online_url": {
                                "url": MOCKED_CREDENTIALS["url"] + "/v4/deployments/55c93e6f-82ac-4d51-a052-4d2249aabe7a/predictions"
                            },
                            "state": "ready"
                        }
                    },
                    "metadata": {
                        "created_at": "2020-06-15T13:48:15.140Z",
                        "guid": "55c93e6f-82ac-4d51-a052-4d2249aabe7a",
                        "href": "/v4/deployments/55c93e6f-82ac-4d51-a052-4d2249aabe7a",
                        "id": "55c93e6f-82ac-4d51-a052-4d2249aabe7a",
                        "modified_at": "2020-06-15T13:48:15.352Z",
                        "name": "Notebook import additional data",
                        "parent": {
                            "href": ""
                        }
                    }
                }
            ]
        }

        expected = "{'error': None, 'info': None, 'status': 'ok'}"
        response = get_info()

        assert isinstance(response, ServerInfo)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["url"] + '/v4/deployments?version=2020-10-20&space_id=space_id', data={}, headers=mock.ANY)

    @mock_wml_credentials('info_controller')
    @mock.patch("swagger_server.controllers.info_controller.requests.request")
    def test_get_info_error(self, mock_request, mock_cred):
        """Test case for get_info

        Get Server Information and Status
        """
        mock_request.side_effect = KeyError('foo')

        expected = '{\'error\': "<class \'KeyError\'>", \'info\': None, \'status\': \'error\'}'
        response = get_info()

        assert isinstance(response, ServerInfo)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["url"] + '/v4/deployments?version=2020-10-20&space_id=space_id', data={}, headers=mock.ANY)


if __name__ == '__main__':
    import unittest
    unittest.main()
