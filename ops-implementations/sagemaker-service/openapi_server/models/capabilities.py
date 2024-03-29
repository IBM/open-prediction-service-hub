# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.capabilities_managed_capabilities import CapabilitiesManagedCapabilities
from openapi_server.models.capability import Capability
from openapi_server import util

from openapi_server.models.capabilities_managed_capabilities import CapabilitiesManagedCapabilities  # noqa: E501
from openapi_server.models.capability import Capability  # noqa: E501

class Capabilities(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, capabilities=None, managed_capabilities=None):  # noqa: E501
        """Capabilities - a model defined in OpenAPI

        :param capabilities: The capabilities of this Capabilities.  # noqa: E501
        :type capabilities: List[Capability]
        :param managed_capabilities: The managed_capabilities of this Capabilities.  # noqa: E501
        :type managed_capabilities: CapabilitiesManagedCapabilities
        """
        self.openapi_types = {
            'capabilities': List[Capability],
            'managed_capabilities': CapabilitiesManagedCapabilities
        }

        self.attribute_map = {
            'capabilities': 'capabilities',
            'managed_capabilities': 'managed_capabilities'
        }

        self._capabilities = capabilities
        self._managed_capabilities = managed_capabilities

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

    @property
    def managed_capabilities(self):
        """Gets the managed_capabilities of this Capabilities.


        :return: The managed_capabilities of this Capabilities.
        :rtype: CapabilitiesManagedCapabilities
        """
        return self._managed_capabilities

    @managed_capabilities.setter
    def managed_capabilities(self, managed_capabilities):
        """Sets the managed_capabilities of this Capabilities.


        :param managed_capabilities: The managed_capabilities of this Capabilities.
        :type managed_capabilities: CapabilitiesManagedCapabilities
        """

        self._managed_capabilities = managed_capabilities
