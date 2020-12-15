import requests
import warnings
import pytest
import urllib.parse
import os
import json
import logging
from jsonschema import validate

SPEC_RELATIVE_PATH = './../open-prediction-service.yaml'


class TestOPSApi():

    CAPABILITIES_ENDPOINT = '/capabilities'
    MODELS_ENDPOINT = '/models'
    RUN_ENDPOINT = '/predictions'

    # {
    #     "info": {
    #         "description": "Open Prediction Service for Scikit Learn models based on OPSv2 API"
    #     },
    #    "status": "ok"
    # }
    def test_get_info(self, url):
        request_url = urllib.parse.urljoin(url, '/info')
        response = requests.get(request_url)
        assert response.status_code == 200

        logging.debug(response.json())

        assert response.json()['status'] == 'ok'

    def test_has_info_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, self.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        logging.debug(response.json())

        assert 'info' in response.json()['capabilities']

    def test_has_discover_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, self.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        logging.debug(response.json())

        assert 'discover' in response.json()['capabilities']

    def test_has_run_capabilities(self, url):
        request_url = urllib.parse.urljoin(url, self.CAPABILITIES_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        logging.debug(response.json())

        assert 'run' in response.json()['capabilities']

    def get_first_model(self, url):
        request_url = urllib.parse.urljoin(url, self.MODELS_ENDPOINT)
        response = requests.get(request_url)
        models = response.json()['models']
        return models[0]

    def test_can_list_models(self, url):
        request_url = urllib.parse.urljoin(url, self.MODELS_ENDPOINT)
        response = requests.get(request_url)
        assert response.status_code == 200

        logging.debug(response.json())

        models = response.json()['models']
        assert len(models) > 1

    def test_models_and_endpoints_have_required_fields(self, url):
        request_url = urllib.parse.urljoin(url, self.MODELS_ENDPOINT)
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
                self.get_and_validate_endpoint(endpoint_href, model_href)

    def get_and_validate_endpoint(self, endpoint_href, model_href):
        response = requests.get(endpoint_href)
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

    def test_models_and_endpoints_predictions(self, url):
        request_url = urllib.parse.urljoin(url, self.MODELS_ENDPOINT)
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
                request_url = urllib.parse.urljoin(url, self.RUN_ENDPOINT)
                response = requests.post(request_url, json={
                    "parameters": [{
                        "name": "creditScore",
                        "value": 400
                    },
                        {
                        "name": "income",
                        "value": 10000
                    },
                        {
                        "name": "loanAmount",
                        "value": 1000000
                    },
                        {
                        "name": "monthDuration",
                        "value": 12
                    },
                        {
                        "name": "rate",
                        "value": 2
                    }
                    ],
                    "target": [{
                        "href": endpoint_href,
                        "rel": "endpoint"
                    }]
                })

                logging.warning(response.text)

                assert response.status_code == 200

                logging.warning(response.json())
