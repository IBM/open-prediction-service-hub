import connexion
import six

from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoint_creation import EndpointCreation  # noqa: E501
from openapi_server.models.endpoint_update import EndpointUpdate  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.model_creation import ModelCreation  # noqa: E501
from openapi_server.models.model_update import ModelUpdate  # noqa: E501
from openapi_server import util


def add_model(model_creation):  # noqa: E501
    """Add a Model

    Add a Model to the service # noqa: E501

    :param model_creation: 
    :type model_creation: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        model_creation = ModelCreation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_endpoint(endpoint_creation, model_id=None):  # noqa: E501
    """Create Endpoint

    Create a Model Endpoint # noqa: E501

    :param endpoint_creation: Required Endpoint definition
    :type endpoint_creation: dict | bytes
    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoint
    """
    if connexion.request.is_json:
        endpoint_creation = EndpointCreation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_endpoint_by_id(endpoint_id):  # noqa: E501
    """Delete Endpoint by Id

     # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: None
    """
    return 'do some magic!'


def delete_model_by_model_id(model_id):  # noqa: E501
    """Delete Model by Id

    Removes a model specified by Id # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: None
    """
    return 'do some magic!'


def update_endpoint_by_endpoint_id(endpoint_id, endpoint_update=None):  # noqa: E501
    """Update an Endpoint

    update an existing Endpoint in the service # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str
    :param endpoint_update: 
    :type endpoint_update: dict | bytes

    :rtype: Endpoint
    """
    if connexion.request.is_json:
        endpoint_update = EndpointUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_model_by_model_id(model_id, model_update):  # noqa: E501
    """Update a Model

    update an existing Model in the service # noqa: E501

    :param model_id: ID of model
    :type model_id: str
    :param model_update: 
    :type model_update: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        model_update = ModelUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
