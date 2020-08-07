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
from swagger_server.util import get_wml_api_date_version, get_wml_credentials
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.link import Link  # noqa: E501
from swagger_server.models.machine_learning_model import MachineLearningModel  # noqa: E501
from swagger_server.models.machine_learning_model_endpoint import MachineLearningModelEndpoint  # noqa: E501
from swagger_server.models.machine_learning_model_endpoints import MachineLearningModelEndpoints  # noqa: E501
from swagger_server.models.machine_learning_models import MachineLearningModels  # noqa: E501

import requests

STATUS_MAPPER = {
    'initializing': 'creating',
    'updating': 'updating',
    'ready': 'in_service',
    'failed': 'failed'
}


def list_endpoints(model_id=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: MachineLearningModelEndpoints
    """
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()
        url = wml_credentials['url'] + "/v4/deployments" + "?version=" + api_version_date

        payload = {}
        headers = {
            'ML-Instance-ID': wml_credentials['instance_id'],
            'Authorization': 'Bearer ' + wml_credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()

        endpoints = response.json()["resources"]
        endpoints_list = []

        def append_endpoint(endpoint_el):
            endpoints_list.append(
                MachineLearningModelEndpoint(
                    id=endpoint_el['metadata']['id'],
                    name=endpoint_el['metadata']['name'],
                    status=STATUS_MAPPER[endpoint_el['entity']['status']['state']],
                    deployed_at=endpoint_el['metadata']['created_at'],
                    links=[
                        Link(
                            rel='self',
                            href=endpoint_el['metadata']['id']
                        ),
                        Link(
                            rel='model',
                            href=endpoint_el['entity']['asset']['id']
                        )
                    ]
                )
            )

        for endpoint in endpoints:
            if model_id == None:
                append_endpoint(endpoint)
            else:
                if endpoint['entity']['asset']['id'] == model_id:
                    append_endpoint(endpoint)

        return MachineLearningModelEndpoints(endpoints=endpoints_list)
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))


def list_models():  # noqa: E501
    """List Models

    Returns the list of ML models. # noqa: E501


    :rtype: MachineLearningModels
    """
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()

        url = wml_credentials['url'] + "/v4/models" + "?version=" + api_version_date

        payload = {}
        headers = {
            'ML-Instance-ID': wml_credentials['instance_id'],
            'Authorization': 'Bearer ' + wml_credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        models = response.json()["resources"]

        model_list = []
        for model in models:
            model_list.append(
                MachineLearningModel(
                    id=model['metadata']['id'],
                    name=model['metadata']['name'],
                    input_schema= (
                        model['entity']['schemas']['input'][0]['fields']
                        if len(model['entity']['schemas']['input']) > 0
                           and 'fields' in model['entity']['schemas']['input'][0]
                        else {}
                    ),
                    output_schema= (
                        model['entity']['schemas']['output'][0]['fields']
                        if len(model['entity']['schemas']['output']) > 0
                           and 'fields' in model['entity']['schemas']['output'][0]
                        else {}
                    ),
                    created_at=model['metadata']['created_at'],
                    modified_at=model['metadata']['modified_at'],
                    version=model['metadata']['rev'],
                    links=[
                        Link(
                            rel='self',
                            href=model['metadata']['id']
                        )
                    ]
                )
            )
        return MachineLearningModels(models=model_list)
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))
