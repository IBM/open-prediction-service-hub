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
import typing
from types import SimpleNamespace

import boto3
import botocore
from flask import request

import openapi_server.models as openapi_models

statusMapper = {
    'OutOfService': 'out_of_service',
    'Creating': 'creating',
    'Updating': 'updating',
    'SystemUpdating': 'under_maintenance',
    'RollingBack': 'rolling_back',
    'InService': 'in_service',
    'Deleting': 'deleting',
    'Failed': 'failed'
}


def retrieve_endpoint_data(client, endpoint_name):
    endpoint_details = client.describe_endpoint(EndpointName=endpoint_name)
    endpoint_config = endpoint_details['EndpointConfigName']
    endpoint_config_details = client.describe_endpoint_config(EndpointConfigName=endpoint_config)
    # Support for 1 endpoint hosting multiple models
    model_names = []
    for model in endpoint_config_details['ProductionVariants']:
        model_names.append(model['ModelName'])

    return dict(
        endpoint_details=endpoint_details,
        endpoint_config_details=endpoint_config_details,
        model_names=model_names
    )


def do_for_each_endpoint(client, callback):
    endpoints = client.list_endpoints()['Endpoints']
    for endpoint in endpoints:
        # For every endpoint (deployed model) retrieve model name
        endpoint_name = endpoint['EndpointName']
        endpoint_data = SimpleNamespace(**retrieve_endpoint_data(client, endpoint_name))
        dict_element = dict(
            endpoint_name=endpoint_name,
            endpoint_details=endpoint_data.endpoint_details,
            endpoint_config_details=endpoint_data.endpoint_config_details,
            model_names=endpoint_data.model_names
        )
        callback(**dict_element)


def get_endpoint_by_id(endpoint_id):  # noqa: E501
    """Get an Endpoint

    Returns an ML endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    root_url = request.url_root
    try:
        client = boto3.client('sagemaker')
        endpoint_data = SimpleNamespace(**retrieve_endpoint_data(client, endpoint_id))

        links = [
            openapi_models.Link(
                rel='self',
                href=root_url + 'endpoints/' + endpoint_id
            )
        ]
        for model_name in endpoint_data.model_names:
            links.append(
                openapi_models.Link(
                    rel='model',
                    href=root_url + 'models/' + model_name
                )
            )

        return openapi_models.Endpoint(
            id=endpoint_id,
            name=endpoint_id,
            status=statusMapper[endpoint_data.endpoint_details['EndpointStatus']],
            deployed_at=endpoint_data.endpoint_details['CreationTime'],
            links=links
        )
    except botocore.exceptions.ClientError as error:
        return openapi_models.Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.Error(error=str(sys.exc_info()[0]))


def get_model_by_id(model_id):  # noqa: E501
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    root_url = request.url_root
    try:
        client = boto3.client('sagemaker')
        model = client.describe_model(ModelName=model_id)

        links = [
            openapi_models.Link(
                rel='self',
                href=root_url + 'models/' + model_id
            )
        ]

        def callback_for_each_endpoints(endpoint_name, model_names, **__):
            if model_id in model_names:
                links.append(
                    openapi_models.Link(
                        rel='endpoint',
                        href=root_url + 'endpoints/' + endpoint_name
                    )
                )

        do_for_each_endpoint(client, callback_for_each_endpoints)

        return openapi_models.Model(
            id=model['ModelName'],
            name=model['ModelName'],
            created_at=model['CreationTime'],
            links=links
        )
    except botocore.exceptions.ClientError as error:
        return openapi_models.Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.Error(error=str(sys.exc_info()[0]))


def list_endpoints(model_id=None, limit=50, offset=0, total_count=False):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoints
    """
    root_url = request.url_root
    try:
        client = boto3.client('sagemaker')

        endpoints_list = []

        def append_endpoint(endpoint_name, endpoint_details, model_names):

            links = [
                openapi_models.Link(
                    rel='self',
                    href=root_url + 'endpoints/' + endpoint_name
                )
            ]
            for model_name in model_names:
                links.append(
                    openapi_models.Link(
                        rel='model',
                        href=root_url + 'models/' + model_name
                    )
                )

            endpoints_list.append(
                openapi_models.Endpoint(
                    id=endpoint_name,
                    name=endpoint_name,
                    status=statusMapper[endpoint_details['EndpointStatus']],
                    deployed_at=endpoint_details['CreationTime'],
                    links=links
                )
            )

        def callback_for_each_endpoints(model_names, endpoint_name, endpoint_details, **__):
            if model_id is None:
                append_endpoint(endpoint_name, endpoint_details, model_names)
            else:
                if model_id in model_names:
                    append_endpoint(endpoint_name, endpoint_details, model_names)

        do_for_each_endpoint(client, callback_for_each_endpoints)

        paginated_endpoint_list, count = paginated_resp(endpoints_list, limit, offset, total_count)
        return openapi_models.Endpoints(endpoints=paginated_endpoint_list, total_count=count)
    except botocore.exceptions.ClientError as error:
        return openapi_models.Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.Error(error=str(sys.exc_info()[0]))


def list_models(limit=50, offset=0, total_count=False):  # noqa: E501
    """List Models

    Returns the list of ML models. # noqa: E501


    :rtype: Models
    """
    root_url = request.url_root
    try:
        client = boto3.client('sagemaker')
        models = client.list_models()['Models']

        links_by_model = {}

        def callback_for_each_endpoints(endpoint_name, model_names, **__):
            link_tmp = openapi_models.Link(
                rel='endpoint',
                href=root_url + 'endpoints/' + endpoint_name
            )
            for model_name in model_names:
                if model_name in links_by_model.keys():
                    links_by_model[model_name].append(link_tmp)
                else:
                    links_by_model[model_name] = [link_tmp]

        do_for_each_endpoint(client, callback_for_each_endpoints)

        model_list = []
        for model in models:
            model_name = model['ModelName']

            link = openapi_models.Link(
                rel='self',
                href=root_url + 'models/' + model_name
            )
            if model_name in links_by_model.keys():
                links_by_model[model_name].insert(0, link)
            else:
                links_by_model[model_name] = [link]

            model_list.append(
                openapi_models.Model(
                    id=model_name,
                    name=model_name,
                    created_at=model['CreationTime'],
                    links=links_by_model[model_name]
                )
            )
        paginated_model_list, count = paginated_resp(model_list, limit, offset, total_count)
        return openapi_models.Models(models=paginated_model_list, total_count=count)
    except botocore.exceptions.ClientError as error:
        return openapi_models.Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.Error(error=str(sys.exc_info()[0]))


def paginated_resp(pre_pagination: typing.List, limit: int = 100, offset: int = 0, total_count: bool = False):
    # Openapi default is not used during unit test
    limit = limit or 100
    offset = offset or 0
    total_count = total_count or False

    count = 0 if not total_count else len(pre_pagination)
    start = offset if offset < len(pre_pagination) else len(pre_pagination)
    end = offset + limit if offset + limit < len(pre_pagination) else len(pre_pagination)
    filtered = pre_pagination[start:end]
    return filtered, count
