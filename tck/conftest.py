# content of conftest.py
import urllib.parse

import pytest
import requests

import numpy as np
import pandas as pd
import sklearn.ensemble as skl_ensemble

CAPABILITIES_ENDPOINT = '/capabilities'
INFO_ENDPOINT = '/info'
MODELS_ENDPOINT = '/models'
RUN_ENDPOINT = '/predictions'


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="http://localhost:8080/", help="service URL"
    )


def pytest_configure():
    pytest.CAPABILITIES_ENDPOINT = CAPABILITIES_ENDPOINT
    pytest.INFO_ENDPOINT = INFO_ENDPOINT
    pytest.MODELS_ENDPOINT = MODELS_ENDPOINT
    pytest.RUN_ENDPOINT = RUN_ENDPOINT


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def skip_manage_capability_for_proxy(url):
    request_url = urllib.parse.urljoin(url, CAPABILITIES_ENDPOINT)
    response = requests.get(request_url)
    assert response.status_code == 200
    if 'manage' not in response.json()['capabilities']:
        pytest.skip('Tested service do not provide manage capability')


@pytest.fixture
def regression_predictor() -> skl_ensemble.RandomForestRegressor:
    classifier = skl_ensemble.RandomForestRegressor(random_state=42)
    x_random = pd.DataFrame(data=np.random.rand(20, 2), columns=['x', 'y'])
    y_random = np.random.rand(20)
    classifier.fit(x_random, y_random)
    return classifier
