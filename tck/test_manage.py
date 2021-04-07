import logging
import pathlib
import pickle
import urllib.parse

import pytest
import requests

LOGGER = logging.getLogger(__name__)


class TestManageSection:
    model_json = {
        "name": "test model creation",
        "input_schema": [
            {
                "name": "paramater-1",
                "order": 0,
                "type": "double"
            },
            {
                "name": "paramater-2",
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

    def test_model_creation_deletion(self, url, skip_manage_capability_for_proxy):
        request_url = urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT)

        response = requests.post(request_url, json=self.model_json)

        assert response.status_code == 201

        model_created = response.json()

        assert self.model_json['name'] == model_created['name']

        # delete model
        request_url = urllib.parse.urljoin(
            request_url, pytest.MODELS_ENDPOINT + '/' + model_created['id'])

        LOGGER.warning(request_url)

        response = requests.delete(request_url)

        assert response.status_code == 204

    def test_add_pickle(self, url, regression_predictor, skip_manage_capability_for_proxy):
        model_create_response = requests.post(urllib.parse.urljoin(url, pytest.MODELS_ENDPOINT), json=self.model_json)
        assert model_create_response.status_code == 201
        model_created = model_create_response.json()

        binary_upload_response = requests.post(
            urllib.parse.urljoin(url, f'{pytest.MODELS_ENDPOINT}/{model_created["id"]}'),
            files={'file': pickle.dumps(regression_predictor)},
            data={
                'input_data_structure': 'auto',
                'output_data_structure': 'auto',
                'format': 'joblib'
            }
        )
        assert binary_upload_response.status_code == 201

        model_get_resp = requests.get(urllib.parse.urljoin(url, f'{pytest.MODELS_ENDPOINT}/{model_created["id"]}'))
        model_get = model_get_resp.json()
        endpoint_resources = (link for link in model_get['links'] if link['rel'] == 'endpoint')
        endpoint_resource = next(endpoint_resources, None)
        endpoint_resource_second = next(endpoint_resources, None)
        assert endpoint_resource is not None
        assert endpoint_resource_second is None

        prediction_resp = requests.post(urllib.parse.urljoin(url, pytest.RUN_ENDPOINT), json={
            "parameters": [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            "target": [{
                "href": endpoint_resource['href'],
                "rel": "endpoint"
            }]
        })
        assert prediction_resp.status_code == 200
        assert prediction_resp.json()['result']['predictions'] is not None
        assert type(prediction_resp.json()['result']['predictions']) is float

        response_del = requests.delete(urllib.parse.urljoin(url, f'{pytest.MODELS_ENDPOINT}/{model_created["id"]}'))
        assert response_del.status_code == 204

    def test_upload(self, url, skip_manage_capability_for_proxy):
        model_path = pathlib.Path(__file__).resolve().parent.joinpath('model.pmml')
        with model_path.open(mode='r') as fd:
            model = fd.read()

        upload_response = requests.post(
            urllib.parse.urljoin(url, f'{pytest.UPLOAD_ENDPOINT}'),
            files={'file': ('model.pmml', model)},
            data={
                'format': 'pmml',
                'name': 'test-model'
            }
        )
        assert upload_response.status_code == 201

        model_created = upload_response.json()

        assert model_created['name'] == 'test-model'
        assert model_created['input_schema'] == [
            {
                "name": "creditScore",
                "order": 0,
                "type": "double"
            },
            {
                "name": "income",
                "order": 1,
                "type": "double"
            },
            {
                "name": "loanAmount",
                "order": 2,
                "type": "double"
            },
            {
                "name": "monthDuration",
                "order": 3,
                "type": "double"
            },
            {
                "name": "rate",
                "order": 4,
                "type": "double"
            },
            {
                "name": "yearlyReimbursement",
                "order": 5,
                "type": "double"
            }
        ]
        assert model_created['output_schema'] == {
            "predicted_paymentDefault": {
                "type": "integer"
            },
            "probability_1": {
                "type": "double"
            },
            "probability_0": {
                "type": "double"
            }
        }
