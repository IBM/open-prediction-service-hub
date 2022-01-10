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

import swagger_server.services.discovery as discovery_service
from swagger_server.models.endpoint import Endpoint  # noqa: E501
from swagger_server.models.endpoints import Endpoints  # noqa: E501
from swagger_server.models.model import Model  # noqa: E501
from swagger_server.models.models import Models  # noqa: E501


def get_endpoint_by_id(endpoint_id):  # noqa: E501
    """Get an Endpoint

    Returns an ML endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    return discovery_service.get_endpoint_by_id(endpoint_id)


def get_model_by_id(model_id):  # noqa: E501
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    return discovery_service.get_model_by_id(model_id)


def list_endpoints(model_id=None, limit=None, offset=None, total_count=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoints
    """
    return discovery_service.list_models(model_id, limit, offset, total_count)


def list_models(limit=50, offset=0, total_count=False):  # noqa: E501
    """List Models

    Returns the list of ML models. # noqa: E501


    :rtype: Models
    """
    return discovery_service.list_models(limit, offset, total_count)
