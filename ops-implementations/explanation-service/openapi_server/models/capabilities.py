# coding: utf-8

from __future__ import absolute_import

from typing import List

from openapi_server.models.base_model_ import Model
from openapi_server.models.capability import Capability
from openapi_server import util


class Capabilities(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, capabilities=None):  # noqa: E501
        """Capabilities - a model defined in OpenAPI

        :param capabilities: The capabilities of this Capabilities.  # noqa: E501
        :type capabilities: List[Capability]
        """
        self.openapi_types = {
            'capabilities': List[Capability]
        }

        self.attribute_map = {
            'capabilities': 'capabilities'
        }

        self._capabilities = capabilities

    @classmethod
    def from_dict(cls, dikt) -> 'Capabilities':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Capabilities of this Capabilities.  # noqa: E501
        :rtype: Capabilities
        """
        return util.deserialize_model(dikt, cls)

    @property
    def capabilities(self):
        """Gets the capabilities of this Capabilities.

        Capabilities of the service  # noqa: E501

        :return: The capabilities of this Capabilities.
        :rtype: List[Capability]
        """
        return self._capabilities

    @capabilities.setter
    def capabilities(self, capabilities):
        """Sets the capabilities of this Capabilities.

        Capabilities of the service  # noqa: E501

        :param capabilities: The capabilities of this Capabilities.
        :type capabilities: List[Capability]
        """
        if capabilities is None:
            raise ValueError("Invalid value for `capabilities`, must not be `None`")  # noqa: E501

        self._capabilities = capabilities
