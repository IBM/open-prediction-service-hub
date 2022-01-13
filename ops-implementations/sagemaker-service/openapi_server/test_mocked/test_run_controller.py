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

from unittest import mock

import botocore
from botocore.response import StreamingBody

import numpy as np


from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.parameter import Parameter  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.models.prediction import Prediction  # noqa: E501
from openapi_server.models.prediction_response import PredictionResponse  # noqa: E501
from openapi_server.test import BaseTestCase

from openapi_server.controllers.run_controller import prediction


class TestRunController(BaseTestCase):
    """RunController integration test stubs"""

    @mock.patch("openapi_server.services.run.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.run.boto3.client")
    def test_prediction(self, mock_boto_client, mock_invoke_endpoint):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_boto_client.return_value = botocore.client.BaseClient()
        buffer = BytesIO()
        x = np.array(['this on returned', 2, 3])
        np.save(buffer, x)
        body = StreamingBody(BytesIO(buffer.getvalue()), len(buffer.getvalue()))

        mock_invoke_endpoint.return_value.invoke_endpoint.return_value = {
            'Body': body,
            'ContentType': 'application/x-npy',
            'InvokedProductionVariant': 'string',
            'CustomAttributes': 'string'
        }

        body = Prediction(parameters=[Parameter(name='name', value='toto')], target=[Link(rel='endpoint', href='toto')])

        expected = "{'result': {'predictions': 'this on returned'}}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, PredictionResponse)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker-runtime')
        mock_invoke_endpoint.assert_called_once()

    @mock.patch("openapi_server.services.run.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.run.boto3.client")
    def test_prediction_no_endpoint_in_target(self, mock_boto_client, mock_invoke_endpoint):
        """Test case for prediction

        Call Prediction of specified deployment
        """

        body = Prediction(parameters=[Parameter(name='name', value='toto')], target=[Link(rel='noEndpoint', href='toto')])

        expected = "{'error': 'endpoint should be provided in target array'}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_not_called()
        mock_invoke_endpoint.assert_not_called()

    @mock.patch("openapi_server.services.run.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.run.boto3.client")
    def test_prediction_client_error(self, mock_boto_client, mock_invoke_endpoint):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_invoke_endpoint.return_value.invoke_endpoint.side_effect = botocore.exceptions.ClientError(
            error_response={'Error': {'Code': 'ErrorCode'}},
            operation_name='invoke_endpoint'
        )

        body = Prediction(parameters=[Parameter(name='name', value='toto')], target=[Link(rel='endpoint', href='toto')])

        expected = "{'error': 'An error occurred (ErrorCode) when calling the invoke_endpoint '\n" + \
                   "          'operation: Unknown'}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker-runtime')
        mock_invoke_endpoint.assert_called_once()

    @mock.patch("openapi_server.services.run.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.run.boto3.client")
    def test_prediction_param_validation_error(self, mock_boto_client, mock_invoke_endpoint):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_invoke_endpoint.return_value.invoke_endpoint.side_effect = botocore.exceptions.ParamValidationError(
            report='param error'
        )

        body = Prediction(parameters=[Parameter(name='name', value='toto')], target=[Link(rel='endpoint', href='toto')])

        expected = "{'error': 'Parameter validation failed:\\nparam error'}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker-runtime')
        mock_invoke_endpoint.assert_called_once()

    @mock.patch("openapi_server.services.run.botocore.client.BaseClient")
    @mock.patch("openapi_server.services.run.boto3.client")
    def test_prediction_unknown_error(self, mock_boto_client, mock_invoke_endpoint):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_boto_client.return_value = botocore.client.BaseClient()

        mock_invoke_endpoint.return_value.invoke_endpoint.side_effect = {
            'error': 'error message'
        }

        body = Prediction(parameters=[Parameter(name='name', value='toto')], target=[Link(rel='endpoint', href='toto')])

        expected = "{'error': \"<class 'TypeError'>\"}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'

        mock_boto_client.assert_called_once_with('sagemaker-runtime')
        mock_invoke_endpoint.assert_called_once()


if __name__ == '__main__':
    import unittest
    unittest.main()
