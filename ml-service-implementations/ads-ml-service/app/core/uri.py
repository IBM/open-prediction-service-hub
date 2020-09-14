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


import re

# TEMPLATE = 'ops:///{resource_type}/{resource_id}'  #  OPS specific uri scheme is not used
TEMPLATE = '/{resource_type}/{resource_id}'
RE_TEMPLATE = r'^(?P<scheme>[a-zA-Z0-9+.-]+)?(?:\://)?[^/]*(?P<resource_path>.*)/(?P<resource_id>.*)$'
ADS_ML_SERVICE_RE = re.compile(RE_TEMPLATE)
