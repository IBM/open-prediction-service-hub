# coding: utf-8

from __future__ import absolute_import

import unittest
from datetime import datetime
from unittest import mock

from unittest.mock import ANY
import os
import requests

from swagger_server.controllers.discover_controller import list_endpoints, list_models
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.machine_learning_model_endpoints import MachineLearningModelEndpoints  # noqa: E501
from swagger_server.models.machine_learning_models import MachineLearningModels  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.test_mocked.util import mock_wml_env, MOCKED_CREDENTIALS

class TestDiscoverController(BaseTestCase, unittest.TestCase):
    """DiscoverController integration test stubs"""

    # LIST ENDPOINTS
    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
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

        expected = ("{'endpoints': [{'deployed_at': '2020-06-15T13:48:15.140Z',\n" +
                    "                'id': '55c93e6f-82ac-4d51-a052-4d2249aabe7a',\n" +
                    "                'links': [{'href': '55c93e6f-82ac-4d51-a052-4d2249aabe7a',\n" +
                    "                           'rel': 'self'},\n" +
                    "                          {'href': '51bafd0b-3f8d-45e3-a5ec-a50612360706',\n" +
                    "                           'rel': 'model'}],\n" +
                    "                'name': 'Notebook import additional data',\n" +
                    "                'status': 'in_service'}]}")

        response = list_endpoints()

        assert isinstance(response, MachineLearningModelEndpoints)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints_with_model_id(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
        """
        modelId = 'FakeModelId'

        mock_request.return_value.json.return_value = {
            "resources": [
                {
                    "entity": {
                        "asset": {
                            "href": "/v3/ml_assets/models/59dac523-e5e0-452b-aa04-50a144beced5/versions/51bafd0b-3f8d-45e3-a5ec-a50612360706",
                            "id": modelId
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

        expected = ("{'endpoints': [{'deployed_at': '2020-06-15T13:48:15.140Z',\n" +
                    "                'id': '55c93e6f-82ac-4d51-a052-4d2249aabe7a',\n" +
                    "                'links': [{'href': '55c93e6f-82ac-4d51-a052-4d2249aabe7a',\n" +
                    "                           'rel': 'self'},\n" +
                    "                          {'href': 'FakeModelId', 'rel': 'model'}],\n" +
                    "                'name': 'Notebook import additional data',\n" +
                    "                'status': 'in_service'}]}")

        response = list_endpoints(modelId)

        assert isinstance(response, MachineLearningModelEndpoints)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints_not_existing_model_id(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
        """
        modelId = 'FakeModelId'

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

        expected = ("{'endpoints': []}")

        response = list_endpoints(modelId)

        assert isinstance(response, MachineLearningModelEndpoints)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints_http_error(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_request.return_value.json.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        response = list_endpoints()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints_request_error(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_request.return_value.json.side_effect = requests.exceptions.RequestException("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        response = list_endpoints()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_endpoints_unknown_error(self, mock_request):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_request.return_value.json.side_effect = {
            'error': 'error message'
        }

        expected = '{\'error\': "<class \'TypeError\'>"}'
        response = list_endpoints()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/deployments?version=2020-08-07', data={}, headers=ANY)

    # LIST MODELS
    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_models(self, mock_request):
        """Test case for list_models

        List Models
        """
        mock_request.return_value.json.return_value = {
            "resources": [
                {
                    "metadata": {
                        "name": "Bank marketing (sample) test - P8 LGBMClassifierEstimator",
                        "guid": "4cd4e9fa-e8b0-47e4-95e4-a881a6f6f791",
                        "rev": "d89e325a-c51d-48ef-9600-c4f064dae20f",
                        "id": "4cd4e9fa-e8b0-47e4-95e4-a881a6f6f791",
                        "modified_at": "2020-06-05T07:20:15.802Z",
                        "created_at": "2020-06-05T07:20:15.760Z",
                        "href": "/v4/models/4cd4e9fa-e8b0-47e4-95e4-a881a6f6f791?rev=d89e325a-c51d-48ef-9600-c4f064dae20f"
                    },
                    "entity": {
                        "name": "Bank marketing (sample) test - P8 LGBMClassifierEstimator",
                        "tags": [
                            {
                                "value": "dsx-autoai",
                                "description": "An identifier for distinguishing v4 models imported from Watson Studio AutoAI"
                            },
                            {
                                "value": "dsx-project.25f0bdf1-42b4-4277-b312-e44d0fb22bfd",
                                "description": "guid of associated DSX project"
                            }
                        ],
                        "content_status": {
                            "state": "persisted"
                        },
                        "pipeline": {
                            "id": "3d9a5179-3427-4531-b5e9-9c72e2da0fc4",
                            "href": "/v4/pipelines/3d9a5179-3427-4531-b5e9-9c72e2da0fc4?rev=fc547a55-3b2b-486c-88ed-17314fe2caf2",
                            "rev": "fc547a55-3b2b-486c-88ed-17314fe2caf2"
                        },
                        "import": {
                            "location": {
                                "bucket": "daxweatherprojecttest-donotdelete-pr-hrn0dc04uetoqa",
                                "path": "auto_ml/af5703fc-19ec-4a40-a420-9ac7624fc4b7/wml_data/45337a4c-f2fc-4137-ad7b-3baa99ed8847/data/automl/hpo_c_output/Pipeline5/model.pickle"
                            },
                            "type": "s3",
                            "connection": {
                                "access_key_id": "5abdbfa5a8854f78b27edc400ac54b30",
                                "secret_access_key": "e11f8dd26ad61fdbd688ffaf39a07ab6494a5a9eb4188a8f",
                                "endpoint_url": "https://s3.eu-geo.objectstorage.softlayer.net"
                            }
                        },
                        "space": {
                            "id": "e838650c-28a2-499a-a269-456da2699768",
                            "href": "/v4/spaces/e838650c-28a2-499a-a269-456da2699768"
                        },
                        "type": "wml-hybrid_0.1",
                        "runtime": {
                            "id": "hybrid_0.1",
                            "href": "/v4/runtimes/hybrid_0.1"
                        },
                        "schemas": {
                            "input": [
                                {
                                    "id": "auto_ai_kb_input_schema",
                                    "fields": [
                                        {
                                            "name": "age",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "job",
                                            "type": "object"
                                        },
                                        {
                                            "name": "marital",
                                            "type": "object"
                                        },
                                        {
                                            "name": "education",
                                            "type": "object"
                                        },
                                        {
                                            "name": "default",
                                            "type": "object"
                                        },
                                        {
                                            "name": "balance",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "housing",
                                            "type": "object"
                                        },
                                        {
                                            "name": "loan",
                                            "type": "object"
                                        },
                                        {
                                            "name": "contact",
                                            "type": "object"
                                        },
                                        {
                                            "name": "day",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "month",
                                            "type": "object"
                                        },
                                        {
                                            "name": "duration",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "campaign",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "pdays",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "previous",
                                            "type": "int64"
                                        },
                                        {
                                            "name": "poutcome",
                                            "type": "object"
                                        }
                                    ]
                                }
                            ],
                            "output": []
                        }
                    }
                }
            ]
        }

        expected = ("{'links': None,\n" +
                    " 'models': [{'created_at': '2020-06-05T07:20:15.760Z',\n" +
                    "             'id': '4cd4e9fa-e8b0-47e4-95e4-a881a6f6f791',\n" +
                    "             'input_schema': [{'name': 'age', 'type': 'int64'},\n" +
                    "                              {'name': 'job', 'type': 'object'},\n" +
                    "                              {'name': 'marital', 'type': 'object'},\n" +
                    "                              {'name': 'education', 'type': 'object'},\n" +
                    "                              {'name': 'default', 'type': 'object'},\n" +
                    "                              {'name': 'balance', 'type': 'int64'},\n" +
                    "                              {'name': 'housing', 'type': 'object'},\n" +
                    "                              {'name': 'loan', 'type': 'object'},\n" +
                    "                              {'name': 'contact', 'type': 'object'},\n" +
                    "                              {'name': 'day', 'type': 'int64'},\n" +
                    "                              {'name': 'month', 'type': 'object'},\n" +
                    "                              {'name': 'duration', 'type': 'int64'},\n" +
                    "                              {'name': 'campaign', 'type': 'int64'},\n" +
                    "                              {'name': 'pdays', 'type': 'int64'},\n" +
                    "                              {'name': 'previous', 'type': 'int64'},\n" +
                    "                              {'name': 'poutcome', 'type': 'object'}],\n" +
                    "             'links': [{'href': '4cd4e9fa-e8b0-47e4-95e4-a881a6f6f791',\n" +
                    "                        'rel': 'self'}],\n" +
                    "             'modified_at': '2020-06-05T07:20:15.802Z',\n" +
                    "             'name': 'Bank marketing (sample) test - P8 '\n" +
                    "                     'LGBMClassifierEstimator',\n" +
                    "             'output_schema': {},\n" +
                    "             'version': 'd89e325a-c51d-48ef-9600-c4f064dae20f'}]}")

        response = list_models()

        assert isinstance(response, MachineLearningModels)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/models?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_models_http_error(self, mock_request):
        """Test case for list_models

        List Models
        """
        mock_request.return_value.json.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        response = list_models()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/models?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_models_request_error(self, mock_request):
        """Test case for list_models

        List Models
        """
        mock_request.return_value.json.side_effect = requests.exceptions.RequestException("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        response = list_models()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/models?version=2020-08-07', data={}, headers=ANY)

    @mock_wml_env()
    @mock.patch("swagger_server.controllers.discover_controller.requests.request")
    def test_list_models_unknown_error(self, mock_request):
        """Test case for list_models

        List Models
        """
        mock_request.return_value.json.side_effect = {
            'error': 'error message'
        }

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = list_models()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("GET", MOCKED_CREDENTIALS["WML_URL"] + '/v4/models?version=2020-08-07', data={}, headers=ANY)


if __name__ == '__main__':
    import unittest

    unittest.main()
