# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.endpoint_all_of import EndpointAllOf
from openapi_server.models.endpoint_creation import EndpointCreation
from openapi_server.models.link import Link
from openapi_server import util

from openapi_server.models.endpoint_all_of import EndpointAllOf  # noqa: E501
from openapi_server.models.endpoint_creation import EndpointCreation  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501

class Endpoint(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, status=None, links=None, id=None, deployed_at=None):  # noqa: E501
        """Endpoint - a model defined in OpenAPI

        :param name: The name of this Endpoint.  # noqa: E501
        :type name: str
        :param status: The status of this Endpoint.  # noqa: E501
        :type status: str
        :param links: The links of this Endpoint.  # noqa: E501
        :type links: List[Link]
        :param id: The id of this Endpoint.  # noqa: E501
        :type id: str
        :param deployed_at: The deployed_at of this Endpoint.  # noqa: E501
        :type deployed_at: datetime
        """
        self.openapi_types = {
            'name': str,
            'status': str,
            'links': List[Link],
            'id': str,
            'deployed_at': datetime
        }

        self.attribute_map = {
            'name': 'name',
            'status': 'status',
            'links': 'links',
            'id': 'id',
            'deployed_at': 'deployed_at'
        }

        self._name = name
        self._status = status
        self._links = links
        self._id = id
        self._deployed_at = deployed_at

    @classmethod
    def from_dict(cls, dikt) -> 'Endpoint':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Endpoint of this Endpoint.  # noqa: E501
        :rtype: Endpoint
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this Endpoint.

        Name of Version  # noqa: E501

        :return: The name of this Endpoint.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Endpoint.

        Name of Version  # noqa: E501

        :param name: The name of this Endpoint.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def status(self):
        """Gets the status of this Endpoint.

        Status of the Endpoint  # noqa: E501

        :return: The status of this Endpoint.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Endpoint.

        Status of the Endpoint  # noqa: E501

        :param status: The status of this Endpoint.
        :type status: str
        """
        allowed_values = ["out_of_service", "creating", "updating", "under_maintenance", "rolling_back", "in_service", "deleting", "failed"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def links(self):
        """Gets the links of this Endpoint.

        Optional array of typed linked resources  # noqa: E501

        :return: The links of this Endpoint.
        :rtype: List[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Endpoint.

        Optional array of typed linked resources  # noqa: E501

        :param links: The links of this Endpoint.
        :type links: List[Link]
        """

        self._links = links

    @property
    def id(self):
        """Gets the id of this Endpoint.

        Id of Version  # noqa: E501

        :return: The id of this Endpoint.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Endpoint.

        Id of Version  # noqa: E501

        :param id: The id of this Endpoint.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def deployed_at(self):
        """Gets the deployed_at of this Endpoint.

        date of the Version  # noqa: E501

        :return: The deployed_at of this Endpoint.
        :rtype: datetime
        """
        return self._deployed_at

    @deployed_at.setter
    def deployed_at(self, deployed_at):
        """Sets the deployed_at of this Endpoint.

        date of the Version  # noqa: E501

        :param deployed_at: The deployed_at of this Endpoint.
        :type deployed_at: datetime
        """
        if deployed_at is None:
            raise ValueError("Invalid value for `deployed_at`, must not be `None`")  # noqa: E501

        self._deployed_at = deployed_at
