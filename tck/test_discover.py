import urllib.parse
import logging

import pytest
import requests

LOGGER = logging.getLogger(__name__)


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
