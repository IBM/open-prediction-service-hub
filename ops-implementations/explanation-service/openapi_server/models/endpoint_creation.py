# coding: utf-8

from __future__ import absolute_import

from typing import List

from openapi_server.models.base_model_ import Model
from openapi_server.models.link import Link
from openapi_server import util


class EndpointCreation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, status=None, links=None):  # noqa: E501
        """EndpointCreation - a model defined in OpenAPI

        :param name: The name of this EndpointCreation.  # noqa: E501
        :type name: str
        :param status: The status of this EndpointCreation.  # noqa: E501
        :type status: str
        :param links: The links of this EndpointCreation.  # noqa: E501
        :type links: List[Link]
        """
        self.openapi_types = {
            'name': str,
            'status': str,
            'links': List[Link]
        }

        self.attribute_map = {
            'name': 'name',
            'status': 'status',
            'links': 'links'
        }

        self._name = name
        self._status = status
        self._links = links

    @classmethod
    def from_dict(cls, dikt) -> 'EndpointCreation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EndpointCreation of this EndpointCreation.  # noqa: E501
        :rtype: EndpointCreation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this EndpointCreation.

        Name of Version  # noqa: E501

        :return: The name of this EndpointCreation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EndpointCreation.

        Name of Version  # noqa: E501

        :param name: The name of this EndpointCreation.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def status(self):
        """Gets the status of this EndpointCreation.

        Status of the Endpoint  # noqa: E501

        :return: The status of this EndpointCreation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this EndpointCreation.

        Status of the Endpoint  # noqa: E501

        :param status: The status of this EndpointCreation.
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
        """Gets the links of this EndpointCreation.

        Optional array of typed linked resources  # noqa: E501

        :return: The links of this EndpointCreation.
        :rtype: List[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this EndpointCreation.

        Optional array of typed linked resources  # noqa: E501

        :param links: The links of this EndpointCreation.
        :type links: List[Link]
        """

        self._links = links