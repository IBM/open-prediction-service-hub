import urllib.parse
import logging

import pytest
import requests

LOGGER = logging.getLogger(__name__)


class TestInfoSection:

    # {
    #     "info": {
    #         "description": "Open Prediction Service for Scikit Learn models based on OPSv2 API"
    #     },
    #    "status": "ok"
    # }
    def test_get_info(self, url):
        request_url = urllib.parse.urljoin(url, pytest.INFO_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        LOGGER.debug(response.json())

        assert response.json()['status'] == 'ok'

    def test_has_info_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, pytest.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        LOGGER.debug(response.json())

        assert 'info' in response.json()['capabilities']

    def test_has_discover_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, pytest.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        LOGGER.debug(response.json())

        assert 'discover' in response.json()['capabilities']

    def test_has_run_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, pytest.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        LOGGER.debug(response.json())

        assert 'run' in response.json()['capabilities']
