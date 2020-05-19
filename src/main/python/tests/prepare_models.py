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


import logging
import os
import subprocess
import sys
from pathlib import Path

EXAMPLES_ROOT = Path(__file__).resolve().parents[4].joinpath('examples')


def __deploy(directory: Path, archive: Path) -> Path:
    logger = logging.getLogger(__name__)

    if archive.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.info(f'model {archive} exists. set EML_RETRAIN_MODELS to re-train')
        return archive

    subprocess.run(
        ['python3', str(directory.joinpath('training.py'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    subprocess.run(
        ['python3', str(directory.joinpath('deployment.py'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return archive


def miniloan_linear_svc_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification', 'miniloan_linear_svc')
    archive = directory.joinpath('miniloan-linear-svc-archive.pkl')

    return __deploy(directory, archive)


def miniloan_xgb_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification', 'miniloan_xgb')
    archive = directory.joinpath('miniloan-xgb-archive.pkl')

    return __deploy(directory, archive)


def miniloan_rfc_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath(
        'model_training_and_deployment', 'classification_with_probabilities', 'miniloan_rfc')
    archive = directory.joinpath('miniloan-rfc-archive.pkl')

    return __deploy(directory, archive)


def miniloan_rfr_pickle() -> Path:
    directory = EXAMPLES_ROOT.joinpath('model_training_and_deployment', 'regression', 'miniloan_rfr')
    archive = directory.joinpath('miniloan-rfr-archive.pkl')

    return __deploy(directory, archive)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    miniloan_linear_svc_pickle()
    miniloan_rfc_pickle()
    miniloan_rfr_pickle()
    miniloan_xgb_pickle()
