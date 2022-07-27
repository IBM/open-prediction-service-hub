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
import subprocess

PYPMML_VERSIONS = [
    '0.9.16',
    '0.9.15',
    '0.9.12',
    '0.9.11',
    '0.9.10',
    '0.9.9',
    '0.9.7',
    '0.9.6',
    '0.9.5',
    '0.9.4',
    '0.9.3',
    '0.9.2',
    '0.9.1',
    '0.9.0'
]

PY4J_VERSIONS = [
    '0.10.9.5',
    '0.10.9.4',
    '0.10.9.3',
    '0.10.9.2',
    '0.10.9.1',
    '0.10.9',
    '0.10.8.1',
    '0.10.7',
    '0.10.6',
    '0.10.5',
    '0.10.4',
    '0.10.3',
    '0.10.2.1',
    '0.10.2',
    '0.10.1',
    '0.10.0',
    '0.9.2',
    '0.9.1',
    '0.9'
]


def find_dep():
    build_path = pathlib.Path(__file__).resolve().parents[1]
    template_path = build_path / 'scripts' / 'requirements-template.txt'
    requirements_path = build_path / 'requirements.txt'

    template_content = template_path.read_text()
    total = len(PYPMML_VERSIONS) * len(PY4J_VERSIONS)
    counter = 0

    for pypmml_version in PYPMML_VERSIONS:
        for py4j_version in PY4J_VERSIONS:
            requirement = template_content.format(pypmml_version=pypmml_version, py4j_version=py4j_version)
            requirements_path.write_text(requirement)

            print(f'total: {total}, counter: {counter}, percentage: {counter / total}')
            print(f'pypmml_version: {pypmml_version}')
            print(f'py4j_version: {py4j_version}')

            result_build = subprocess.run(
                ["docker", "build", '-t', 'ads-ml-service:latest', str(build_path)], capture_output=True, text=True)

            if result_build.returncode != 0:
                print('build failure')
                print(result_build.stdout)
                print(result_build.stderr)
                continue
            else:
                print('build success')

            result_test = subprocess.run(
                ["docker", "run", '--rm', '--entrypoint', 'python3', '--name', 'test-py4j', 'ads-ml-service:latest',
                 '-m', 'pytest', '-v', 'app/tests'], capture_output=True, text=True)
            if result_test.returncode != 0:
                print('test failure')
                print(result_test.stdout)
            else:
                print(result_test.stdout)
                print('Found compatible libraries')
                return

            del_image_result = subprocess.run(
                ["docker", 'rmi', 'ads-ml-service:latest'], capture_output=True, text=True)
            if del_image_result.returncode != 0:
                print('Del image failure')
            else:
                print('Del image success')

            if counter % 15 == 0:
                prune_image_result = subprocess.run(
                    ["docker", 'system', 'prune', '-af'], capture_output=True, text=True)
                if prune_image_result.returncode != 0:
                    print('Prune image failure')
                    print(prune_image_result.stdout)
                    print(prune_image_result.stderr)
                else:
                    print('Prune image success')

            counter += 1


if __name__ == '__main__':
    find_dep()
