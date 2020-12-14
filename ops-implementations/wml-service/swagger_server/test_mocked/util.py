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

from unittest import mock

import os


MOCKED_CREDENTIALS_VARS = {
    "WML_AUTH_URL": "https://iam.cloud.ibm.com/identity/token",
    "WML_API_KEY": "apikey",
    "WML_SPACE_ID": "space_id",
    "WML_URL": "url"
}

MOCKED_CREDENTIALS = {
    "token": "token",
    "space_id": MOCKED_CREDENTIALS_VARS["WML_SPACE_ID"],
    "url": MOCKED_CREDENTIALS_VARS["WML_URL"]
}


def mock_wml_env():
    return mock.patch.dict(os.environ, MOCKED_CREDENTIALS_VARS)


def mock_wml_credentials(controller):
    return mock.patch("swagger_server.controllers." + controller + ".get_wml_credentials",
                      return_value=MOCKED_CREDENTIALS)

