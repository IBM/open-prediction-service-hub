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


import app.models.metadata as app_model_metadata


def test_patch_metadata():
    current = {
        'a': 1,
        'b': 2,
        'c': {
            'c1': 1,
            'c2': 2
        }
    }
    patch_1 = {
        'b': 3
    }
    patch_2 = {
        'c': {
            'c1': 3,
        }
    }
    assert app_model_metadata.patch_metadata(current, patch_1) == {
        'a': 1,
        'b': 3,
        'c': {
            'c1': 1,
            'c2': 2
        }
    }
    assert app_model_metadata.patch_metadata(current, patch_2) == {
        'a': 1,
        'b': 2,
        'c': {
            'c1': 3,
        }
    }
