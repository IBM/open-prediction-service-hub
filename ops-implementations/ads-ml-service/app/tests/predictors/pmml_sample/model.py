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


import pathlib


def get_pmml_file() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.joinpath('model.pmml')


def get_pmml_no_output_schema_file() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.joinpath('model-no-output-schema.pmml')
