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


import typing

import pytest

import app.core.uri as ops_uri


@pytest.mark.parametrize(
    'uri, expected',
    [
        ('ops:///endpoints/1', ('/endpoints', 1)),
        ('ops:///models/25', ('/models', 25))
    ]
)
def test_parse_uri_resources(uri: typing.Text, expected: typing.Tuple[typing.Text, int]):
    match = ops_uri.ADS_ML_SERVICE_RE.match(uri)
    resource_path = match.group('resource_path')
    resource_id = int(match.group('resource_id'))

    assert resource_path == expected[0]
    assert resource_id == expected[1]
