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
import pathlib

import fastapi.testclient as testclient


def test_customer_churn_upload(client: testclient.TestClient):
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    customer_churn_model_path = pathlib.Path(__file__).parent / 'wifi.pmml'
    model_creation_resp = client.post(
        url='/upload',
        files={'file': (customer_churn_model_path.name, customer_churn_model_path.read_bytes())}
    )
    assert model_creation_resp is not None
    model_json = model_creation_resp.json()
    assert model_json is not None
    model_id = model_json['id']
    assert model_id is not None

    default_request_path = pathlib.Path(__file__).parent / 'default_rule_wifi.json'

    default_request = json.loads(default_request_path.read_text().replace('endpoint_id', model_id))

    default_response = client.post(url='/predictions', json=default_request)

    assert default_response.status_code == 200

    default_res = default_response.json()

    assert default_res['result']['predicted'] is not None
