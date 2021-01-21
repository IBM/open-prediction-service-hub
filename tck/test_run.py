import logging
import urllib.parse

import pytest
import requests

LOGGER = logging.getLogger(__name__)


class TestRunSection:

    def test_models_and_endpoints_predictions(self, url):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)
        response = requests.get(request_url)

        assert response.status_code == 200

        for model in response.json()['models']:
            assert model['links'] is not None

            endpoint_href = None

            for link in model['links']:
                href = link['href']
                rel = link['rel']

                assert rel is not None
                assert href is not None
                assert rel == 'self' or rel == 'endpoint'

                if rel == 'endpoint':
                    endpoint_href = href

            if endpoint_href:
                request_url = urllib.parse.urljoin(url, pytest.RUN_ENDPOINT)
                response = requests.post(request_url, json={
                    "parameters": self.build_parameters_from_model(model),
                    "target": [{
                        "href": endpoint_href,
                        "rel": "endpoint"
                    }]
                })

                LOGGER.warning(response.json())

                assert response.status_code == 200

    def build_parameters_from_model(self, model):
        parameters = []
        for field in model['input_schema']:
            value = 0
            if field['type'] == 'str' or field['type'] == 'string':
                value = ""
            elif field['type'] == 'bool' or field['type'] == 'boolean':
                value = False
            elif field['type'].startswith('['):
                value = []

            parameters.append({"name": field['name'], "value": value})
        return parameters