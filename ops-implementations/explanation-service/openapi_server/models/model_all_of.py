# coding: utf-8

from __future__ import absolute_import
from datetime import datetime

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ModelAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, created_at=None, modified_at=None):  # noqa: E501
        """ModelAllOf - a model defined in OpenAPI

        :param id: The id of this ModelAllOf.  # noqa: E501
        :type id: str
        :param created_at: The created_at of this ModelAllOf.  # noqa: E501
        :type created_at: datetime
        :param modified_at: The modified_at of this ModelAllOf.  # noqa: E501
        :type modified_at: datetime
        """
        self.openapi_types = {
            'id': str,
            'created_at': datetime,
            'modified_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'created_at': 'created_at',
            'modified_at': 'modified_at'
        }

        self._id = id
        self._created_at = created_at
        self._modified_at = modified_at

    @classmethod
    def from_dict(cls, dikt) -> 'ModelAllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Model_allOf of this ModelAllOf.  # noqa: E501
        :rtype: ModelAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this ModelAllOf.

        ID of model  # noqa: E501

        :return: The id of this ModelAllOf.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelAllOf.

        ID of model  # noqa: E501

        :param id: The id of this ModelAllOf.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this ModelAllOf.

        date of the creation of the model  # noqa: E501

        :return: The created_at of this ModelAllOf.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelAllOf.

        date of the creation of the model  # noqa: E501

        :param created_at: The created_at of this ModelAllOf.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this ModelAllOf.

        date of the update of the model  # noqa: E501

        :return: The modified_at of this ModelAllOf.
        :rtype: datetime
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this ModelAllOf.

        date of the update of the model  # noqa: E501

        :param modified_at: The modified_at of this ModelAllOf.
        :type modified_at: datetime
        """
        if modified_at is None:
            raise ValueError("Invalid value for `modified_at`, must not be `None`")  # noqa: E501

        self._modified_at = modified_at
