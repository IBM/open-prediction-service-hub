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
from pathlib import Path
from typing import Text

from dynamic_hosting import app
from dynamic_hosting.localml import VER
from fastapi.testclient import TestClient
from requests import Response

EXAMPLE_DIR: Path = Path(__file__).resolve().parents[1].joinpath('examples').joinpath('models')

API_VER: Text = f'/v{VER}'


def init():
    os.environ['model_storage'] = str(Path(__file__).resolve().parent.joinpath('storage'))
    client: TestClient = TestClient(app)

    with EXAMPLE_DIR.joinpath('miniloan-lr.pkl').open(mode='rb') as fd:
        res_miniloan_rfc: Response = client.post(
            API_VER + "/models",
            files={'file': fd}
        )

    with EXAMPLE_DIR.joinpath('miniloan-rfc.pkl').open(mode='rb') as fd:
        res_miniloan_lr: Response = client.post(
            API_VER + "/models",
            files={'file': fd}
        )

    with EXAMPLE_DIR.joinpath('miniloan-rfr.pkl').open(mode='rb') as fd:
        res_miniloan_rfr: Response = client.post(
            API_VER + "/models",
            files={'file': fd}
        )

    assert (all([res.status_code == 200 for res in [res_miniloan_rfc, res_miniloan_lr, res_miniloan_rfr]]))


if __name__ == '__main__':
    init()
