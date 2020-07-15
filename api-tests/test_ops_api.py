import requests
import warnings
import pytest
import urllib.parse
import os
import json
from jsonschema import validate

SPEC_RELATIVE_PATH = './../open-prediction-service.json'

class TestOPSApi():

    def get_spec(self):
        current_path = os.path.dirname(os.getenv('PYTEST_CURRENT_TEST').split(':')[0])
        path = os.path.join(current_path, SPEC_RELATIVE_PATH)
        with open(path) as spec:
            spec = json.load(spec)
        return spec

    def test_endpoint_response(self, url):
        print('Trying to reach endpoint')
        assert requests.get(url, verify=False) != ''

    def test_get_models(self, url):
        request_url = urllib.parse.urljoin(url, '/v1/models')
        print('GET - ', request_url)

        response = requests.get(request_url, verify=False)
        data = response.json()

        spec = self.get_spec()

        output_schema = spec["paths"]["/models"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        output_schema["components"] = spec["components"]

        assert response.status_code == 200
        assert isinstance(data, list), "should return list"
        assert len(data) > 0, "WARNING - no models found"
        validate(instance = data, schema = output_schema)

    def test_post_invocation(self, url):
        request_url = urllib.parse.urljoin(url, '/v1/invocations')
        print('POST - ', request_url)

        spec = self.get_spec()

        current_path = os.path.dirname(os.getenv('PYTEST_CURRENT_TEST').split(':')[0])
        body_filename = os.path.join(current_path,'./resources/post_invocation_body.json')
        if not os.path.exists(os.path.dirname(body_filename)):
            os.makedirs(os.path.dirname(body_filename), exist_ok=True)
            example_data = spec["components"]["schemas"]["RequestBody"]["example"]
            with open(body_filename, "w") as f:
                f.write(json.dumps(example_data, indent=4))
            
            assert 0, 'Please fill in ./resources/post_invocation_body.json file with valid body for posting an invocation and try again'
        else :
            with open(body_filename) as json_body:
                data = json.load(json_body)


            input_schema = spec["paths"]["/invocations"]["post"]["requestBody"]["content"]["application/json"]["schema"]
            input_schema["components"] = spec["components"]

            validate(instance = data, schema = input_schema)

            response = requests.post(request_url, data=json.dumps(data), verify=False)
            data = response.json()

            output_schema = spec["paths"]["/invocations"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
            output_schema["components"] = spec["components"]

            assert response.status_code == 200
            assert isinstance(data, object), "should return object"
            validate(instance = data, schema = output_schema)