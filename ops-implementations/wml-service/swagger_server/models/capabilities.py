# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.capability import Capability  # noqa: F401,E501
from swagger_server import util


class Capabilities(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, capabilities: List[Capability]=None):  # noqa: E501
        """Capabilities - a model defined in Swagger

        :param capabilities: The capabilities of this Capabilities.  # noqa: E501
        :type capabilities: List[Capability]
        """
        self.swagger_types = {
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
    def capabilities(self) -> List[Capability]:
        """Gets the capabilities of this Capabilities.

        Capabilities of the service  # noqa: E501

        :return: The capabilities of this Capabilities.
        :rtype: List[Capability]
        """
        return self._capabilities

    @capabilities.setter
    def capabilities(self, capabilities: List[Capability]):
        """Sets the capabilities of this Capabilities.

        Capabilities of the service  # noqa: E501

        :param capabilities: The capabilities of this Capabilities.
        :type capabilities: List[Capability]
        """
        if capabilities is None:
            raise ValueError("Invalid value for `capabilities`, must not be `None`")  # noqa: E501

        self._capabilities = capabilities
