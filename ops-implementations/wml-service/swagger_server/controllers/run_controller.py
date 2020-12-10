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

import sys
from swagger_server.wml_util import \
    get_wml_credentials, \
    get_wml_api_date_version
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.prediction_response import PredictionResponse  # noqa: E501

import requests
import json

import logging
logger = logging.getLogger(__name__)


def prediction(body):  # noqa: E501
    """Call Prediction of specified deployment

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PredictionResponse
    """
    logger.debug(f'prediction({body})')
    # Retrieve parameters
    req_data = []
    fields_data = []
    for param in body['parameters']:
        req_data.append(param['value'])
        fields_data.append(param['name'])
    data = [req_data]

    # Retrieve target
    endpoint = None
    for target in body['target']:
        if 'rel' in target and target['rel'] == 'endpoint':
            endpoint = target['href']
            if endpoint.startswith('http'):
                endpoint = endpoint[endpoint.rfind('/')+1:]

    if not endpoint:
        return Error(error='endpoint should be provided in target array')

    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()
        url = wml_credentials['url'] + "/v4/deployments/" + endpoint + "/predictions" + \
            "?version=" + api_version_date + \
            "&space_id=" + wml_credentials['space_id']

        payload = {
            "input_data": [
                {
                    "fields": fields_data,
                    "values": data
                }
            ]
        }
        payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + wml_credentials['token']
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()

        result = response.json()["predictions"]
        result = result[0]
        predictions = {}
        for index, field in enumerate(result["fields"]):
            predictions[field] = result["values"][0][index]
        return PredictionResponse(result=dict(predictions))
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))
