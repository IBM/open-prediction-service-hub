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

import requests
from swagger_server.util import get_wml_api_date_version, get_wml_credentials
from swagger_server.models.capabilities import Capabilities  # noqa: E501
from swagger_server.models.capability import Capability  # noqa: E501
from swagger_server.models.server_status import ServerStatus  # noqa: E501


def get_capabilities():  # noqa: E501
    """Get Server Capabilities

    Returns the server capabilities # noqa: E501


    :rtype: Capabilities
    """

    return Capabilities([Capability.STATUS, Capability.DISCOVER, Capability.RUNTIME])


def get_status():  # noqa: E501
    """Get Server Status

    Returns a health check on underlying services availability # noqa: E501


    :rtype: ServerStatus
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
        return ServerStatus(status='ok')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ServerStatus(status='error', error=str(sys.exc_info()[0]))
