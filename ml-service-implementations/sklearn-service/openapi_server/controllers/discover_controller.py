import connexion
import six

from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoints import Endpoints  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.models import Models  # noqa: E501
from openapi_server import util


def get_endpoint_by_id(endpoint_id):  # noqa: E501
    """Get an Endpoint

    Returns an ML Endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    return 'do some magic!'


def get_model_by_id(model_id):  # noqa: E501
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    return 'do some magic!'


def list_endpoints(model_id=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoints
    """
    return 'do some magic!'


def list_models():  # noqa: E501
    """List Models

    Returns the list of ML Models. # noqa: E501


    :rtype: Models
    """
    return 'do some magic!'
