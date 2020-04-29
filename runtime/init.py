#!/usr/bin/env python3

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
