# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.prediction import Prediction  # noqa: E501
from openapi_server.models.prediction_response import PredictionResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestRunController(BaseTestCase):
    """RunController integration test stubs"""

    def test_prediction(self):
        """Test case for prediction

        Call Prediction of specified Endpoint
        """
        prediction = {
  "parameters" : [ {
    "name" : "name",
    "value" : "John Doe"
  }, {
    "name" : "age",
    "value" : 17
  }, {
    "name" : "ofAge",
    "value" : False
  }, {
    "name" : "score",
    "value" : 0.42
  } ],
  "target" : [ {
    "rel" : "endpoint",
    "href" : "http://open-prediction-service.org/endpoints/8c2af534-cdce-11ea-87d0-0242ac130003"
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/predictions',
            method='POST',
            headers=headers,
            data=json.dumps(prediction),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
