#!/usr/bin/env python3
#
# Copyright 2022 IBM
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


import pathlib
import random

import locust

# Usage: python3 -m locust --headless --users=50 --hatch-rate=5 --run-time=2m
#                          --host="http://localhost:8080" --locustfile=locustfile.py

API_VER = 'v1'

TEST_MODEL_PATH = pathlib.Path(__file__).parent.joinpath('model.pmml')
TEST_MODEL_PATH_2 = pathlib.Path(__file__).parent.joinpath('MachineLearningModel.pmml')
TEST_MODEL_NAME = TEST_MODEL_PATH.name
TEST_MODEL_NAME_2 = TEST_MODEL_PATH_2.name
TEST_MODEL_CONTENT = TEST_MODEL_PATH.read_bytes()
TEST_MODEL_CONTENT_2 = TEST_MODEL_PATH_2.read_bytes()


def get_prediction_payload(model_id):
    return {
        'parameters': [
            {
                "name": "creditScore",
                "value": random.randint(100, 800)
            }, {
                "name": "income",
                "value": random.uniform(18_000.0, 80_000.0)
            }, {
                "name": "loanAmount",
                "value": random.uniform(18_000.0, 160_000.0)
            }, {
                "name": "monthDuration",
                "value": random.randint(1, 120)
            }, {
                "name": "rate",
                "value": random.uniform(0.1, 10.0)
            }
        ],
        'target': [
            {
                'rel': 'endpoint',
                'href': f'/endpoints/{model_id}'
            }
        ]
    }


class ApiUser(locust.HttpUser):
    wait_time = locust.between(1.0, 2.0)

    @locust.task(10)
    def read_models(self):
        self.client.get('/models')

    @locust.task(30)
    def upload_then_get_endpoint_then_delete(self):
        model_creation_resp2 = self.client.post(
            url='/upload',
            files={'file': (TEST_MODEL_NAME_2, TEST_MODEL_CONTENT_2)}
        )

        model_json2 = model_creation_resp2.json()
        model_id2 = model_json2['id']

        self.client.get(url=f'/endpoints/{model_id2}', name="/endpoints/[id]")
        self.client.delete(url=f'/models/{model_id2}', name="/models/[id]")

    @locust.task(30)
    def upload_then_predict_then_delete(self):
        model_creation_resp = self.client.post(
            url='/upload',
            files={'file': (TEST_MODEL_NAME, TEST_MODEL_CONTENT)}
        )

        model_json = model_creation_resp.json()
        model_id = model_json['id']
        self.client.post(
            url='/predictions',
            json=get_prediction_payload(model_id)
        )

        self.client.delete(url=f'/models/{model_id}', name="/models/[id]")

    @locust.task(10)
    def invocation(self):
        self.client.post(
            url='/predictions',
            json=get_prediction_payload(random.randint(1, 4))
        )
