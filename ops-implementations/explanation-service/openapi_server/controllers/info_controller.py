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

from openapi_server.models.capabilities import Capabilities  # noqa: E501
from openapi_server.models.capability import Capability  # noqa: E501
from openapi_server.models.server_info import ServerInfo  # noqa: E501


def get_capabilities():  # noqa: E501
    """Get Server Capabilities

    Returns the server capabilities # noqa: E501


    :rtype: Capabilities
    """
    return Capabilities([Capability.INFO, Capability.DISCOVER, Capability.RUN])


def get_info():  # noqa: E501
    """Get Server Information and Status

    Returns a health check of underlying service and additional information # noqa: E501


    :rtype: ServerInfo
    """
    info = dict(
        description='Loan default payment scoring model with explanations',
        specification='Open Prediction Service v2'
    )
    return ServerInfo(status='ok', info={
        'description': info
    })
