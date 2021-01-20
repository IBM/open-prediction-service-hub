import logging
import urllib.parse

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


class TestDiscoverySection:

    def get_first_model(self, url):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)
        response = requests.get(request_url)
        models = response.json()['models']
        return models[0]

    def test_can_list_models(self, url):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        LOGGER.debug(response.json())

        models = response.json()['models']
        assert len(models) > 1

    def test_models_and_endpoints_have_required_fields(self, url):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)
        response = requests.get(request_url)

        assert response.status_code == 200

        for model in response.json()['models']:

            assert model['id'] is not None
            assert model['links'] is not None

            model_href = None
            endpoint_href = None

            for link in model['links']:
                href = link['href']
                rel = link['rel']

                assert rel is not None
                assert href is not None
                assert rel == 'self' or rel == 'endpoint'

                if rel == 'endpoint':
                    endpoint_href = href
                else:
                    model_href = href

            if endpoint_href and model_href:
                self.get_and_validate_endpoint(url, endpoint_href, model_href)

    def get_and_validate_endpoint(self, url, endpoint_href, model_href):
        endpoint_url = endpoint_href
        if not endpoint_url.startswith("http"):
            endpoint_url = urllib.parse.urljoin(url, endpoint_href)

        response = requests.get(endpoint_url)
        assert response.status_code == 200

        endpoint = response.json()

        rel_self_href = None
        rel_model_href = None

        for link in endpoint['links']:
            href = link['href']
            rel = link['rel']

            assert rel is not None
            assert href is not None
            assert rel == 'self' or rel == 'model'

            if rel == 'model':
                rel_model_href = href
            else:
                rel_self_href = href

        assert rel_self_href == endpoint_href
        assert rel_model_href == model_href


class TestManageSection:

    def test_model_creation_deletion(self, url, skip_manage_capability_for_proxy):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)

        model_json = {
            "name": "test model creation",
            "input_schema": [
                {
                    "name": "paramater",
                    "order": 0,
                    "type": "double"
                }
            ],
            "output_schema": {
                "prediction": {
                    "type": "double"
                }
            },
            "version": "v1",
            "metadata": {
                "description": "test model creation description"
            }
        }

        response = requests.post(request_url, json=model_json)

        assert response.status_code == 200

        model_created = response.json()

        assert model_json['name'] == model_created['name']

        # delete model
        request_url = urllib.parse.urljoin(
            request_url, pytest.MODELS_ENDPOINT + '/' + model_created['id'])

        LOGGER.warning(request_url)

        response = requests.delete(request_url)

        assert response.status_code == 204


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
