import connexion
import six

from openapi_server.models.capabilities import Capabilities  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.server_info import ServerInfo  # noqa: E501
from openapi_server import util


def get_capabilities():  # noqa: E501
    """Get Server Capabilities

    Returns the server capabilities # noqa: E501


    :rtype: Capabilities
    """
    return 'do some magic!'


def get_info():  # noqa: E501
    """Get Server Information and Status

    Returns a health check of underlying service and additional information # noqa: E501


    :rtype: ServerInfo
    """
    return 'do some magic!'
