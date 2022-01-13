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

import unittest
from datetime import datetime
from unittest import mock

import botocore
from openapi_server.controllers.discover_controller import list_endpoints, list_models, get_endpoint_by_id, get_model_by_id
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.endpoints import Endpoints
from openapi_server.models.endpoint import Endpoint
from openapi_server.models.models import Models
from openapi_server.models.model import Model
from openapi_server.test import BaseTestCase


class TestDiscoverController(BaseTestCase, unittest.TestCase):
    """DiscoverController integration test stubs"""

    # GET ENDPOINT BY ID
    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_endpoint_by_id(self, mock_boto_client, mock_list_endpoints):
        """Test case for get_endpoint_by_id

        Get an Endpoint
        """
        endpoint_id = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.describe_endpoint.return_value = {
            'EndpointName': 'string',
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }

        mock_list_endpoints.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': 'string',
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'deployed_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    " 'id': 'FakeEndpointId',\n" +
                    " 'links': [{'href': 'http://localhost/endpoints/FakeEndpointId', 'rel': 'self'},\n" +
                    "           {'href': 'http://localhost/models/string', 'rel': 'model'}],\n" +
                    " 'metadata': None,\n" +
                    " 'name': 'FakeEndpointId',\n" +
                    " 'status': 'in_service'}")

        response = get_endpoint_by_id(endpoint_id)

        assert isinstance(response, Endpoint)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_endpoint_by_id_client_error(self, mock_boto_client, mock_list_endpoints):
        """Test case for get_endpoint_by_id

        Get an Endpoint
        """
        endpoint_id = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.describe_endpoint.side_effect = botocore.exceptions.ClientError(
            error_response={'Error': {'Code': 'ErrorCode'}},
            operation_name='describe_endpoint'
        )

        expected = ("{'error': 'An error occurred (ErrorCode) when calling the describe_endpoint '\n" +
                    "          'operation: Unknown'}")

        response = get_endpoint_by_id(endpoint_id)

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_endpoint_by_id_unknown_error(self, mock_boto_client, mock_list_endpoints):
        """Test case for get_endpoint_by_id

        Get an Endpoint
        """
        endpoint_id = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.describe_endpoint.side_effect = {
            'error': 'error message'
        }

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = get_endpoint_by_id(endpoint_id)

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    # GET MODEL BY ID
    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_model_by_id(self, mock_boto_client, mock_client):
        """Test case for get_model_by_id

        Get a Model
        """
        modelId = 'FakeModelId'
        endpointId = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()
        mock_client.return_value.describe_model.return_value = {
            'ModelName': modelId,
            'ModelArn': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        mock_client.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': endpointId,
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                }
            ],
            'NextToken': 'string'
        }
        mock_client.return_value.describe_endpoint.return_value = {
            'EndpointName': endpointId,
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': modelId,
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'created_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    " 'id': 'FakeModelId',\n" +
                    " 'input_schema': None,\n" +
                    " 'links': [{'href': 'http://localhost/models/FakeModelId', 'rel': 'self'},\n" +
                    "           {'href': 'http://localhost/endpoints/FakeEndpointId',\n" +
                    "            'rel': 'endpoint'}],\n" +
                    " 'metadata': None,\n" +
                    " 'modified_at': None,\n" +
                    " 'name': 'FakeModelId',\n" +
                    " 'output_schema': None,\n" +
                    " 'version': None}")

        response = get_model_by_id(modelId)

        assert isinstance(response, Model)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_client.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_model_by_id_client_error(self, mock_boto_client, mock_list_models):
        """Test case for get_model_by_id

         Get a Model
         """
        modelId = 'FakeModelId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_models.return_value.describe_model.side_effect = botocore.exceptions.ClientError(
            error_response={'Error': {'Code': 'ErrorCode'}},
            operation_name='describe_model'
        )

        expected = ("{'error': 'An error occurred (ErrorCode) when calling the describe_model '\n" +
                    "          'operation: Unknown'}")

        response = get_model_by_id(modelId)

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_models.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_get_model_by_id_unknown_error(self, mock_boto_client, mock_list_models):
        """Test case for get_model_by_id

        Get a Model
        """
        modelId = 'FakeModelId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_models.return_value.describe_model.side_effect = {
            'error': 'error message'
        }

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = get_model_by_id(modelId)

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_models.assert_called_once()

    # LIST ENDPOINTS
    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_endpoints(self, mock_boto_client, mock_list_endpoints):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': 'string',
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                },
            ],
            'NextToken': 'string'
        }

        mock_list_endpoints.return_value.describe_endpoint.return_value = {
            'EndpointName': 'string',
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }

        mock_list_endpoints.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': 'string',
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'endpoints': [{'deployed_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    "                'id': 'string',\n" +
                    "                'links': [{'href': 'http://localhost/endpoints/string',\n" +
                    "                           'rel': 'self'},\n" +
                    "                          {'href': 'http://localhost/models/string',\n" +
                    "                           'rel': 'model'}],\n" +
                    "                'metadata': None,\n"
                    "                'name': 'string',\n" +
                    "                'status': 'in_service'}],\n"
                    " 'total_count': 0}")

        response = list_endpoints()

        assert isinstance(response, Endpoints)
        assert str(response) == expected, 'response is not matching expected response'
        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_endpoints_with_model_id(self, mock_boto_client, mock_list_endpoints):
        """Test case for list_endpoints

        List Endpoints
        """
        modelId = 'FakeModelId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': 'string',
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                },
            ],
            'NextToken': 'string'
        }

        mock_list_endpoints.return_value.describe_endpoint.return_value = {
            'EndpointName': 'string',
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }

        mock_list_endpoints.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': modelId,
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'endpoints': [{'deployed_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    "                'id': 'string',\n" +
                    "                'links': [{'href': 'http://localhost/endpoints/string',\n" +
                    "                           'rel': 'self'},\n" +
                    "                          {'href': 'http://localhost/models/FakeModelId',\n" +
                    "                           'rel': 'model'}],\n" +
                    "                'metadata': None,\n" +
                    "                'name': 'string',\n" +
                    "                'status': 'in_service'}],\n"
                    " 'total_count': 0}")

        response = list_endpoints(modelId)

        assert isinstance(response, Endpoints)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_endpoints_not_existing_model_id(self, mock_boto_client, mock_list_endpoints):
        """Test case for list_endpoints

        List Endpoints
        """
        modelId = 'FakeModelId'
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': 'string',
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                },
            ],
            'NextToken': 'string'
        }

        mock_list_endpoints.return_value.describe_endpoint.return_value = {
            'EndpointName': 'string',
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }

        mock_list_endpoints.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': 'NotTheSame',
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = "{'endpoints': [], 'total_count': 0}"

        response = list_endpoints(modelId)

        assert isinstance(response, Endpoints)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_endpoints_client_error(self, mock_boto_client, mock_list_endpoints):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.list_endpoints.side_effect = botocore.exceptions.ClientError(
            error_response={'Error': {'Code': 'ErrorCode'}},
            operation_name='list_endpoints'
        )

        expected = ("{'error': 'An error occurred (ErrorCode) when calling the list_endpoints '\n" +
                    "          'operation: Unknown'}")

        response = list_endpoints()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_endpoints_unknown_error(self, mock_boto_client, mock_list_endpoints):
        """Test case for list_endpoints

        List Endpoints
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_endpoints.return_value.list_endpoints.side_effect = {
            'error': 'error message'
        }

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = list_endpoints()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_endpoints.assert_called_once()

    # LIST MODELS
    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_models(self, mock_boto_client, mock_client):
        """Test case for list_models

        List Models
        """
        modelId = 'FakeModelId'
        endpointId = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()
        mock_client.return_value.list_models.return_value = {
            'Models': [
                {
                    'ModelName': modelId,
                    'ModelArn': 'string',
                    'CreationTime': datetime(2015, 1, 1)
                },
            ],
            'NextToken': 'string'
        }

        mock_client.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': endpointId,
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                }
            ],
            'NextToken': 'string'
        }
        mock_client.return_value.describe_endpoint.return_value = {
            'EndpointName': endpointId,
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': modelId,
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'models': [{'created_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    "             'id': 'FakeModelId',\n" +
                    "             'input_schema': None,\n" +
                    "             'links': [{'href': 'http://localhost/models/FakeModelId',\n" +
                    "                        'rel': 'self'},\n" +
                    "                       {'href': 'http://localhost/endpoints/FakeEndpointId',\n" +
                    "                        'rel': 'endpoint'}],\n" +
                    "             'metadata': None,\n" +
                    "             'modified_at': None,\n" +
                    "             'name': 'FakeModelId',\n" +
                    "             'output_schema': None,\n" +
                    "             'version': None}],\n"
                    " 'total_count': 0}")

        response = list_models()

        assert isinstance(response, Models)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_client.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_models_no_endpoint_for_a_model(self, mock_boto_client, mock_client):
        """Test case for list_models

        List Models
        """
        modelId = 'FakeModelId'
        endpointId = 'FakeEndpointId'
        mock_boto_client.return_value = botocore.client.BaseClient()
        mock_client.return_value.list_models.return_value = {
            'Models': [
                {
                    'ModelName': modelId,
                    'ModelArn': 'string',
                    'CreationTime': datetime(2015, 1, 1)
                },
            ],
            'NextToken': 'string'
        }

        mock_client.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': endpointId,
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                }
            ],
            'NextToken': 'string'
        }
        mock_client.return_value.describe_endpoint.return_value = {
            'EndpointName': endpointId,
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': 'notTheSameModelId',
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'models': [{'created_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    "             'id': 'FakeModelId',\n" +
                    "             'input_schema': None,\n" +
                    "             'links': [{'href': 'http://localhost/models/FakeModelId',\n" +
                    "                        'rel': 'self'}],\n" +
                    "             'metadata': None,\n" +
                    "             'modified_at': None,\n" +
                    "             'name': 'FakeModelId',\n" +
                    "             'output_schema': None,\n" +
                    "             'version': None}],\n" +
                    " 'total_count': 0}")

        response = list_models()

        assert isinstance(response, Models)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_client.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_models_multiple_endpoints_for_a_model(self, mock_boto_client, mock_client):
        """Test case for list_models

        List Models
        """
        modelId = 'FakeModelId'
        endpointId = 'FakeEndpointId'
        endpointId2 = 'FakeEndpointId2'
        mock_boto_client.return_value = botocore.client.BaseClient()
        mock_client.return_value.list_models.return_value = {
            'Models': [
                {
                    'ModelName': modelId,
                    'ModelArn': 'string',
                    'CreationTime': datetime(2015, 1, 1)
                },
            ],
            'NextToken': 'string'
        }

        mock_client.return_value.list_endpoints.return_value = {
            'Endpoints': [
                {
                    'EndpointName': endpointId,
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                },
                {
                    'EndpointName': endpointId2,
                    'EndpointArn': 'string',
                    'CreationTime': datetime(2015, 1, 1),
                    'LastModifiedTime': datetime(2015, 1, 1),
                    'EndpointStatus': 'InService'
                }
            ],
            'NextToken': 'string'
        }
        mock_client.return_value.describe_endpoint.return_value = {
            'EndpointName': endpointId,
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': modelId,
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint.return_value = {
            'EndpointName': endpointId2,
            'EndpointArn': 'string',
            'EndpointConfigName': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'DeployedImages': [
                        {
                            'SpecifiedImage': 'string',
                            'ResolvedImage': 'string',
                            'ResolutionTime': datetime(2015, 1, 1)
                        },
                    ],
                    'CurrentWeight': ...,
                    'DesiredWeight': ...,
                    'CurrentInstanceCount': 123,
                    'DesiredInstanceCount': 123
                },
            ],
            'DataCaptureConfig': {
                'EnableCapture': True | False,
                'CaptureStatus': 'Started',
                'CurrentSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string'
            },
            'EndpointStatus': 'InService',
            'FailureReason': 'string',
            'CreationTime': datetime(2015, 1, 1),
            'LastModifiedTime': datetime(2015, 1, 1)
        }
        mock_client.return_value.describe_endpoint_config.return_value = {
            'EndpointConfigName': 'string',
            'EndpointConfigArn': 'string',
            'ProductionVariants': [
                {
                    'VariantName': 'string',
                    'ModelName': modelId,
                    'InitialInstanceCount': 123,
                    'InstanceType': 'ml.t2.medium',
                    'InitialVariantWeight': ...,
                    'AcceleratorType': 'ml.eia1.medium',
                }
            ],
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 123,
                'DestinationS3Uri': 'string',
                'KmsKeyId': 'string',
                'CaptureOptions': [
                    {
                        'CaptureMode': 'Input'
                    },
                ],
                'CaptureContentTypeHeader': {
                    'CsvContentTypes': [
                        'string',
                    ],
                    'JsonContentTypes': [
                        'string',
                    ]
                }
            },
            'KmsKeyId': 'string',
            'CreationTime': datetime(2015, 1, 1)
        }

        expected = ("{'models': [{'created_at': datetime.datetime(2015, 1, 1, 0, 0),\n" +
                    "             'id': 'FakeModelId',\n" +
                    "             'input_schema': None,\n" +
                    "             'links': [{'href': 'http://localhost/models/FakeModelId',\n" +
                    "                        'rel': 'self'},\n" +
                    "                       {'href': 'http://localhost/endpoints/FakeEndpointId',\n" +
                    "                        'rel': 'endpoint'},\n" +
                    "                       {'href': 'http://localhost/endpoints/FakeEndpointId2',\n" +
                    "                        'rel': 'endpoint'}],\n" +
                    "             'metadata': None,\n" +
                    "             'modified_at': None,\n" +
                    "             'name': 'FakeModelId',\n" +
                    "             'output_schema': None,\n" +
                    "             'version': None}],\n"
                    " 'total_count': 0}")

        response = list_models()

        assert isinstance(response, Models)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_client.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_models_client_error(self, mock_boto_client, mock_list_models):
        """Test case for list_models

        List Models
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_models.return_value.list_models.side_effect = botocore.exceptions.ClientError(
            error_response={'Error': {'Code': 'ErrorCode'}},
            operation_name='list_models'
        )

        expected = ("{'error': 'An error occurred (ErrorCode) when calling the list_models '\n" +
                    "          'operation: Unknown'}")

        response = list_models()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_models.assert_called_once()

    @mock.patch("openapi_server.services.discovery.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.discovery.boto3.client")
    def test_list_models_unknown_error(self, mock_boto_client, mock_list_models):
        """Test case for list_models

        List Models
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_list_models.return_value.list_models.side_effect = {
            'error': 'error message'
        }

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = list_models()

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker')
        mock_list_models.assert_called_once()


if __name__ == '__main__':
    import unittest

    unittest.main()
