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
from swagger_server.wml_util import get_wml_api_date_version, get_wml_credentials
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.link import Link  # noqa: E501
from swagger_server.models.model import Model  # noqa: E501
from swagger_server.models.endpoint import Endpoint  # noqa: E501
from swagger_server.models.endpoints import Endpoints  # noqa: E501
from swagger_server.models.models import Models  # noqa: E501

from flask import request

import requests

STATUS_MAPPER = {
    'initializing': 'creating',
    'updating': 'updating',
    'ready': 'in_service',
    'failed': 'failed'
}


def get_endpoint_by_id(endpoint_id):  # noqa: E501
    """Get an Endpoint

    Returns an ML endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    root_url = request.url_root
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()
        url = wml_credentials['url'] + "/v4/deployments/" + \
            endpoint_id + "?version=" + \
            api_version_date + "&space_id=" + \
            wml_credentials['space_id']

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + wml_credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()

        endpoint = response.json()

        return Endpoint(
            id=endpoint_id,
            name=endpoint['metadata']['name'],
            status=STATUS_MAPPER[endpoint['entity']['status']['state']],
            deployed_at=endpoint['metadata']['created_at'],
            links=[
                Link(
                    rel='self',
                    href=root_url + 'endpoints/' + endpoint_id
                ),
                Link(
                    rel='model',
                    href=root_url + 'models/' + endpoint['entity']['asset']['id']
                )
            ]
        )
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))


def get_model_by_id(model_id):  # noqa: E501
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    root_url = request.url_root
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()

        url = wml_credentials['url'] + "/v4/models/" + model_id + "?version=" + api_version_date + "&space_id=" + \
            wml_credentials['space_id']

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + wml_credentials['token']
        }
        # get all models
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        model = response.json()

        url = wml_credentials['url'] + "/v4/deployments" + "?version=" + api_version_date + "&space_id=" + \
            wml_credentials['space_id'] + "&asset_id=" + model_id

        # get all endpoints for this model asset
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        endpoints = response.json()["resources"]

        # Inserting model link
        links = [
            Link(
                rel='self',
                href=root_url + 'models/' + model_id
            )
        ]

        for endpoint in endpoints:
            links.append(
                Link(
                    rel='endpoint',
                    href=root_url + 'endpoints/' + endpoint['metadata']['id']
                )
            )

        return Model(
            id=model_id,
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
            links=links
        )
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))


def list_endpoints(model_id=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoints
    """
    root_url = request.url_root
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()
        url = wml_credentials['url'] + "/v4/deployments" + "?version=" + api_version_date+ "&space_id=" + \
            wml_credentials['space_id']
        if model_id is not None:
            url += "&asset_id=" + model_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + wml_credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()

        endpoints = response.json()["resources"]
        endpoints_list = []

        for endpoint in endpoints:
            endpoints_list.append(
                Endpoint(
                    id=endpoint['metadata']['id'],
                    name=endpoint['metadata']['name'],
                    status=STATUS_MAPPER[endpoint['entity']['status']['state']],
                    deployed_at=endpoint['metadata']['created_at'],
                    links=[
                        Link(
                            rel='self',
                            href=root_url + 'endpoints/' + endpoint['metadata']['id']
                        ),
                        Link(
                            rel='model',
                            href=root_url + 'models/' + endpoint['entity']['asset']['id']
                        )
                    ]
                )
            )

        return Endpoints(endpoints=endpoints_list)
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


    :rtype: Models
    """
    root_url = request.url_root
    try:
        wml_credentials = get_wml_credentials()
        api_version_date = get_wml_api_date_version()

        url = wml_credentials['url'] + "/v4/models" + "?version=" + api_version_date + "&space_id=" + \
            wml_credentials['space_id']

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + wml_credentials['token']
        }
        # get all models
        response = requests.request("GET", url, headers=headers, data=payload)
        models = response.json()["resources"]

        url = wml_credentials['url'] + "/v4/deployments" + "?version=" + api_version_date + "&space_id=" + \
            wml_credentials['space_id']

        # get all endpoints
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()

        endpoints = response.json()["resources"]

        # create dict mapping model name to endpoint links
        link_by_model = {}

        for endpoint in endpoints:
            endpoint_model_id = endpoint['entity']['asset']['id']
            link = Link(
                rel='endpoint',
                href=root_url + 'endpoints/' + endpoint['metadata']['id']
            )
            if endpoint_model_id in link_by_model:
                link_by_model[endpoint_model_id].append(link)
            else:
                link_by_model[endpoint_model_id] = [link]

        model_list = []
        for model in models:
            model_id = model['metadata']['id']
            # Inserting model link
            link = Link(
                rel='self',
                href=root_url + 'models/' + model_id
            )
            if model_id in link_by_model:
                link_by_model[model_id].insert(0, link)
            else:
                link_by_model[model_id] = [link]

            output_schema = {}
            if len(model['entity']['schemas']['output']) > 0 and 'fields' in model['entity']['schemas']['output'][0]:
                output_schema = {field['name']: {'type': field['type']} for field in (model['entity']['schemas']['output'][0]['fields'])}

            input_schema = []
            if len(model['entity']['schemas']['input']) > 0 and 'fields' in model['entity']['schemas']['input'][0]:
                input_schema = [
                    {'name': field['name'], 'order': i, 'type': field['type']}
                    for i, field in enumerate(model['entity']['schemas']['input'][0]['fields'])
                ]


            model_list.append(
                Model(
                    id=model_id,
                    name=model['metadata']['name'],
                    input_schema=input_schema,
                    output_schema=output_schema,
                    created_at=model['metadata']['created_at'],
                    modified_at=model['metadata']['modified_at'],
                    links=link_by_model[model_id]
                )
            )
        return Models(models=model_list)
    except requests.exceptions.HTTPError as error:
        return Error(error=str(error))
    except requests.exceptions.RequestException as error:
        return Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return Error(error=str(sys.exc_info()[0]))
