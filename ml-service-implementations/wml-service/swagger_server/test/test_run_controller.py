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

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.discrete_parameter import DiscreteParameter # noqa: E501
from swagger_server.models.link import Link  # noqa: E501
from swagger_server.models.prediction import Prediction  # noqa: E501
from swagger_server.models.prediction_response import PredictionResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRunController(BaseTestCase):
    """RunController integration test stubs"""

    def test_prediction(self):
        """Test case for prediction

        Call Prediction of specified deployment
        """
        body = Prediction(parameters=[DiscreteParameter(name='name', value='toto', realtype='DiscreteParameter')], target=[Link(rel='endpoint', href='toto')])
        response = self.client.open(
            '/predictions',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        response_dict_decode = json.loads(response.data.decode('utf-8'))
        prediction_response = PredictionResponse.from_dict(response_dict_decode)
        assert (
                prediction_response.result is not None
                or Error.from_dict(response_dict_decode).error is not None
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
