# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoint_creation import EndpointCreation  # noqa: E501
from openapi_server.models.endpoint_update import EndpointUpdate  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.model_creation import ModelCreation  # noqa: E501
from openapi_server.models.model_update import ModelUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestManageController(BaseTestCase):
    """ManageController integration test stubs"""

    def test_add_model(self):
        """Test case for add_model

        Add a Model
        """
        model_creation = {
  "name" : "Linear regression #1",
  "input_schema" : [ {
    "name" : "feature #1",
    "order" : 1,
    "type" : "integer"
  }, {
    "name" : "feature #2",
    "order" : 2,
    "type" : "double"
  } ],
  "output_schema" : {
    "prediction" : {
      "type" : "string"
    },
    "probability" : {
      "type" : "array",
      "items" : "double"
    },
    "timeElapsed" : {
      "type" : "string",
      "format" : "date-time"
    },
    "inError" : {
      "type" : "boolean"
    }
  },
  "version" : "v0",
  "links" : [ {
    "rel" : "endpoint",
    "href" : "http://open-prediction-service.org/endpoints/841ff27c-cdce-11ea-87d0-0242ac130003"
  }, {
    "rel" : "endpoint",
    "href" : "http://open-prediction-service.org/endpoints/8c2af534-cdce-11ea-87d0-0242ac130003"
  } ],
  "metadata" : {
    "description" : "model description",
    "author" : "admin",
    "metrics" : [ {
      "name" : "accuracy",
      "value" : "0.97"
    } ]
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/models',
            method='POST',
            headers=headers,
            data=json.dumps(model_creation),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_endpoint(self):
        """Test case for create_endpoint

        Create Endpoint
        """
        endpoint_creation = {
  "name" : "South America gigafactory",
  "status" : "in_service",
  "links" : [ {
    "rel" : "model",
    "href" : "http://open-prediction-service.org/models/78bcb500-cdce-11ea-87d0-0242ac130003"
  } ]
}
        query_string = [('model_id', 'model_id_example')]
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/endpoints',
            method='POST',
            headers=headers,
            data=json.dumps(endpoint_creation),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_endpoint_by_id(self):
        """Test case for delete_endpoint_by_id

        Delete Endpoint by Id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/endpoints/{endpoint_id}'.format(endpoint_id='endpoint_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_model_by_model_id(self):
        """Test case for delete_model_by_model_id

        Delete Model by Id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/models/{model_id}'.format(model_id='model_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_endpoint_by_endpoint_id(self):
        """Test case for update_endpoint_by_endpoint_id

        Update an Endpoint
        """
        endpoint_update = {
  "name" : "South America gigafactory",
  "status" : "in_service",
  "links" : [ {
    "rel" : "model",
    "href" : "http://open-prediction-service.org/models/78bcb500-cdce-11ea-87d0-0242ac130003"
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/endpoints/{endpoint_id}'.format(endpoint_id='endpoint_id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(endpoint_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_model_by_model_id(self):
        """Test case for update_model_by_model_id

        Update a Model
        """
        model_update = {
  "name" : "Linear regression #1",
  "input_schema" : [ {
    "name" : "feature #1",
    "order" : 1,
    "type" : "integer"
  }, {
    "name" : "feature #2",
    "order" : 2,
    "type" : "double"
  } ],
  "output_schema" : {
    "prediction" : {
      "type" : "string"
    },
    "probability" : {
      "type" : "array",
      "items" : "double"
    },
    "timeElapsed" : {
      "type" : "string",
      "format" : "date-time"
    },
    "inError" : {
      "type" : "boolean"
    }
  },
  "version" : "v0",
  "links" : [ {
    "rel" : "endpoint",
    "href" : "http://open-prediction-service.org/endpoints/841ff27c-cdce-11ea-87d0-0242ac130003"
  }, {
    "rel" : "endpoint",
    "href" : "http://open-prediction-service.org/endpoints/8c2af534-cdce-11ea-87d0-0242ac130003"
  } ],
  "metadata" : {
    "description" : "model description",
    "author" : "admin",
    "metrics" : [ {
      "name" : "accuracy",
      "value" : "0.97"
    } ]
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/models/{model_id}'.format(model_id='model_id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(model_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
