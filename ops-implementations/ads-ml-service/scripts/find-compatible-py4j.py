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


import json
import os
import pathlib
import subprocess


def find_compatible_py4j():
    build_path = pathlib.Path(__file__).resolve().parents[1]

    template_path = build_path / 'scripts' / 'requirements-template.txt'
    versions_path = build_path / 'scripts' / 'available-versions.json'
    requirements_path = build_path / 'requirements.txt'

    available_versions = json.loads(versions_path.read_text())
    pypmml_versions = available_versions['pypmml']
    py4j_versions = available_versions['py4j']

    total = len(pypmml_versions) * len(py4j_versions)
    counter = 0

    for pypmml_version in pypmml_versions:
        for py4j_version in py4j_versions:
            requirement = template_path.read_text().format(pypmml_version=pypmml_version, py4j_version=py4j_version)
            requirements_path.write_text(requirement)

            print(f'total: {total}, counter: {counter}, percentage: {counter / total}')
            print(f'pypmml_version: {pypmml_version}')
            print(f'py4j_version: {py4j_version}')

            result_test = subprocess.run(["python3", "-m", "tox"], cwd=build_path, capture_output=True, text=True)
            print(os.linesep.join((result_test.stdout.split(os.linesep))[:6]))
            if result_test.returncode != 0:
                print('Not compatible')
            else:
                print('Found compatible combination')
                return

            counter += 1


if __name__ == '__main__':
    find_compatible_py4j()
