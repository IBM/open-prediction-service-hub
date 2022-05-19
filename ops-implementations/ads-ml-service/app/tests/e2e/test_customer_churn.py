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


import json
import math
import pathlib

import fastapi.testclient as testclient


def test_customer_churn_upload(client: testclient.TestClient):
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    customer_churn_model_path = pathlib.Path(__file__).parent / 'Churn_RandomForestClassifier.xml'
    model_creation_resp = client.post(
        url='/upload',
        files={'file': (customer_churn_model_path.name, customer_churn_model_path.read_bytes())}
    )
    assert model_creation_resp is not None
    model_json = model_creation_resp.json()
    assert model_json is not None
    model_id = model_json['id']
    assert model_id is not None

    john_request_path = pathlib.Path(__file__).parent / 'John_churn_request.json'
    peter_request_path = pathlib.Path(__file__).parent / 'Peter_churn_request.json'

    john_request = json.loads(john_request_path.read_text().replace('endpoint_id', model_id))
    peter_request = json.loads(peter_request_path.read_text().replace('endpoint_id', model_id))

    john_response = client.post(url='/predictions', json=john_request)
    peter_response = client.post(url='/predictions', json=peter_request)

    assert john_response.status_code == 200
    assert peter_response.status_code == 200

    john_res = john_response.json()
    peter_res = peter_response.json()

    assert math.isclose(sum([john_res['result']['probability(F)'], john_res['result']['probability(T)']]), 1.0)
    assert math.isclose(sum([peter_res['result']['probability(F)'], peter_res['result']['probability(T)']]), 1.0)
