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

import swagger_server.services.info as info_service


def get_capabilities():  # noqa: E501
    """Get Server Capabilities

    Returns the server capabilities # noqa: E501


    :rtype: Capabilities
    """
    return info_service.get_capabilities()


def get_info():  # noqa: E501
    """Get Server Information and Status

    Returns a health check of underlying service and additional information # noqa: E501


    :rtype: ServerInfo
    """
    return info_service.get_info()
