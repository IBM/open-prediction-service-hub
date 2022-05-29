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


import fastapi.testclient as testclient


def test_customer_churn_upload(client: testclient.TestClient):
    # act
    cap_resp = client.get(url='/capabilities')
    cap = cap_resp.json()

    # assert
    assert cap is not None
    assert cap == {
        'capabilities': [
            'info',
            'discover',
            'manage',
            'run'
        ],
        'managed_capabilities': {
            'supported_input_data_structure': [
                'auto',
                'DataFrame',
                'ndarray',
                'DMatrix',
                'list'
            ],
            'supported_output_data_structure': [
                'auto',
                'DataFrame',
                'ndarray',
                'list'
            ],
            'supported_binary_format': [
                'pickle',
                'joblib',
                'pmml',
                'bst'
            ],
            'supported_upload_format': [
                'pmml'
            ],
            'file_size_limit': 0,
            'unknown_file_size': True
        }
    }
