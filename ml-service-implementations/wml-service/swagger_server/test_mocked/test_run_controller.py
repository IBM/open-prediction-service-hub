# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from unittest import mock

# import botocore
# from botocore.response import StreamingBody
#
# import numpy as np
import requests

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.parameter import Parameter  # noqa: E501
from swagger_server.models.link import Link  # noqa: E501
from swagger_server.models.prediction import Prediction  # noqa: E501
from swagger_server.models.prediction_response import PredictionResponse  # noqa: E501
from swagger_server.test import BaseTestCase

from swagger_server.controllers.run_controller import prediction
from swagger_server.test_mocked.util import mock_wml_credentials, MOCKED_CREDENTIALS


class TestRunController(BaseTestCase):
    """RunController integration test stubs"""

    @mock_wml_credentials('run_controller')
    @mock.patch("swagger_server.controllers.run_controller.requests.request")
    def test_prediction(self, mock_request, mock_cred):
        """Test case for prediction

        Call Prediction of specified deployment
        """

        mock_request.return_value.json.return_value = {
            "predictions": [
                {
                    "fields": [
                        "prediction",
                        "probability"
                    ],
                    "values": [
                        [
                            1,
                            [
                                0.0,
                                1.0
                            ]
                        ]
                    ]
                }
            ]
        }

        body = Prediction(parameters=[Parameter(name='name', value=5)], target=[Link(rel='endpoint', href='toto')])

        expected = "{'result': {'prediction': 1, 'probability': [0.0, 1.0]}}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, PredictionResponse)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("POST", MOCKED_CREDENTIALS["url"] + '/v4/deployments/toto/predictions', data='{"input_data": [{"fields": ["name"], "values": [[5]]}]}', headers=mock.ANY)

    @mock_wml_credentials('run_controller')
    @mock.patch("swagger_server.controllers.run_controller.requests.request")
    def test_prediction_no_endpoint_in_target(self, mock_request, mock_cred):
        """Test case for prediction

        Call Prediction of specified deployment
        """

        body = Prediction(parameters=[Parameter(name='name', value=5)], target=[Link(rel='noEndpoint', href='toto')])

        expected = "{'error': 'endpoint should be provided in target array'}"

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'
        assert not mock_cred.called

        mock_request.assert_not_called()

    @mock_wml_credentials('run_controller')
    @mock.patch("swagger_server.controllers.run_controller.requests.request")
    def test_prediction_http_error(self, mock_request, mock_cred):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_request.return_value.json.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        body = Prediction(parameters=[Parameter(name='name', value=5)], target=[Link(rel='endpoint', href='toto')])

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("POST", MOCKED_CREDENTIALS["url"] + '/v4/deployments/toto/predictions', data='{"input_data": [{"fields": ["name"], "values": [[5]]}]}', headers=mock.ANY)

    @mock_wml_credentials('run_controller')
    @mock.patch("swagger_server.controllers.run_controller.requests.request")
    def test_prediction_request_error(self, mock_request, mock_cred):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_request.return_value.json.side_effect = requests.exceptions.RequestException("401 Client Error: Unauthorized")

        expected = ("{'error': '401 Client Error: Unauthorized'}")

        body = Prediction(parameters=[Parameter(name='name', value=5)], target=[Link(rel='endpoint', href='toto')])

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("POST", MOCKED_CREDENTIALS["url"] + '/v4/deployments/toto/predictions', data='{"input_data": [{"fields": ["name"], "values": [[5]]}]}', headers=mock.ANY)

    @mock_wml_credentials('run_controller')
    @mock.patch("swagger_server.controllers.run_controller.requests.request")
    def test_prediction_unknown_error(self, mock_request, mock_cred):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        mock_request.return_value.json.side_effect = {
            'error': 'error message'
        }

        expected = '{\'error\': "<class \'TypeError\'>"}'

        body = Prediction(parameters=[Parameter(name='name', value=5)], target=[Link(rel='endpoint', href='toto')])

        response = prediction(json.loads(json.dumps(body)))

        assert isinstance(response, Error)
        assert str(response) == expected, 'response is not matching expected response'
        assert mock_cred.called

        mock_request.assert_called_once_with("POST", MOCKED_CREDENTIALS["url"] + '/v4/deployments/toto/predictions', data='{"input_data": [{"fields": ["name"], "values": [[5]]}]}', headers=mock.ANY)


if __name__ == '__main__':
    import unittest
    unittest.main()
