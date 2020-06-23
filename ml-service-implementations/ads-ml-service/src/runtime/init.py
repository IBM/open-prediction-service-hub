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


import os
import subprocess
from pathlib import Path
from typing import Text, List

from predictions.localml import app
from predictions.localml import VER
from fastapi.testclient import TestClient
from requests import Response

API_VER: Text = f'/v{VER}'
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def init():
    os.environ['model_storage'] = str(Path(__file__).resolve().parent.joinpath('storage'))
    client: TestClient = TestClient(app)

    subprocess.run(
        ['python3', str(PROJECT_ROOT.joinpath('tests', 'prepare_models.py'))],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


    models = PROJECT_ROOT.joinpath('examples').rglob('miniloan-*-archive.pkl')
    results = []
    for p in models:
        with p.open(mode='rb') as fd:
            res: Response = client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        results.append(res)

    assert (all([res.status_code == 200 for res in results]))


if __name__ == '__main__':
    init()
