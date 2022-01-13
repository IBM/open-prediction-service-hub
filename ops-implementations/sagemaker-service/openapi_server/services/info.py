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

import boto3

import openapi_server.models as openapi_models


def get_capabilities():  # noqa: E501
    """Get Server Capabilities

    Returns the server capabilities # noqa: E501


    :rtype: Capabilities
    """

    return openapi_models.Capabilities(
        [openapi_models.Capability.INFO, openapi_models.Capability.DISCOVER, openapi_models.Capability.RUN]
    )


def get_info():  # noqa: E501
    """Get Server Information and Status

    Returns a health check of underlying service and additional information # noqa: E501


    :rtype: ServerInfo
    """
    info = dict(
        description='Open Prediction Service for Amazon Sagemaker based on OPSv2 API'
    )
    try:
        boto3.client('sagemaker')
        return openapi_models.ServerInfo(status='ok', info=info)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.ServerInfo(status='error', info=info, error=str(sys.exc_info()[0]))
