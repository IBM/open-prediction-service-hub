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
import pathlib


def test_import_custom_model():
    custom_module_path = pathlib.Path(__file__).resolve().parents[3].joinpath('custom_modules')
    sys.path.append(str(custom_module_path))
    
    import example_custom_predictor as example
    assert example.IdentityPredictor is not None
