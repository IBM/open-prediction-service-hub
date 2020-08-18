# coding: utf-8

from __future__ import absolute_import

from unittest import mock

from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.capability import Capability  # noqa: E501
from swagger_server.models.server_status import ServerStatus  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.controllers.status_controller import get_capabilities, get_status

from swagger_server.test_mocked.util import mock_wml_env, MOCKED_CREDENTIALS

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
    @mock_wml_env()
    @mock.patch("swagger_server.controllers.status_controller.requests.request")
    def test_get_status(self, mock_request):
        """Test case for get_status

        Get Server Status
        """
        mock_request.return_value.json.return_value = {
            "resources": [
                {
                    "entity": {
                        "asset": {
                            "href": "/v3/ml_assets/models/59dac523-e5e0-452b-aa04-50a144beced5/versions/51bafd0b-3f8d-45e3-a5ec-a50612360706",
                            "id": "51bafd0b-3f8d-45e3-a5ec-a50612360706"
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
                                "url": MOCKED_CREDENTIALS["WML_URL"] + "/v4/deployments/55c93e6f-82ac-4d51-a052-4d2249aabe7a/predictions"
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

        expected = "{'error': None, 'status': 'ok'}"
        response = get_status()

        assert isinstance(response, ServerStatus)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=mock.ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.status_controller.requests.request")
    def test_get_status_error(self, mock_request):
        """Test case for get_status

        Get Server Status
        """
        mock_request.side_effect = KeyError('foo')

        expected = "{\'error\': \"<class \'KeyError\'>\", \'status\': \'error\'}"
        response = get_status()

        assert isinstance(response, ServerStatus)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=mock.ANY)


if __name__ == '__main__':
    import unittest
    unittest.main()
