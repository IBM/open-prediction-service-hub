# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.endpoint import Endpoint
from openapi_server import util

from openapi_server.models.endpoint import Endpoint  # noqa: E501

class Endpoints(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, endpoints=None):  # noqa: E501
        """Endpoints - a model defined in OpenAPI

        :param endpoints: The endpoints of this Endpoints.  # noqa: E501
        :type endpoints: List[Endpoint]
        """
        self.openapi_types = {
            'endpoints': List[Endpoint]
        }

        self.attribute_map = {
            'endpoints': 'endpoints'
        }

        self._endpoints = endpoints

    @classmethod
    def from_dict(cls, dikt) -> 'Endpoints':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Endpoints of this Endpoints.  # noqa: E501
        :rtype: Endpoints
        """
        return util.deserialize_model(dikt, cls)

    @property
    def endpoints(self):
        """Gets the endpoints of this Endpoints.

        List of Endpoints  # noqa: E501

        :return: The endpoints of this Endpoints.
        :rtype: List[Endpoint]
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """Sets the endpoints of this Endpoints.

        List of Endpoints  # noqa: E501

        :param endpoints: The endpoints of this Endpoints.
        :type endpoints: List[Endpoint]
        """

        self._endpoints = endpoints
