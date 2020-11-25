import connexion
import six

from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoints import Endpoints  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.models import Models  # noqa: E501
from openapi_server import util
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.controllers.helper import supported_models, get_model_conf  # noqa: E501
from flask import request

def model_id_to_endpoint(model_id):
    endpoint_parameters=get_model_conf(model_id)["endpoint"]
    links = [Link('self', f"{request.url_root}{path}/{model_id}") for path in ["endpoints","models"]]
    return Endpoint(links=links,**endpoint_parameters)

def model_id_to_model(model_id):
    model_parameters=get_model_conf(model_id)["model"]
    links = [Link('self', f"{request.url_root}{path}/{model_id}") for path in ["endpoints","models"]]
    return Model(links=links,**model_parameters)

def get_endpoint_by_id(endpoint_id):  # noqa: E501
    """Get an Endpoint

    Returns an ML Endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    if not endpoint_id in supported_models:
        return Error("endpoint not available")
    return model_id_to_endpoint(endpoint_id)


def get_model_by_id(model_id):  # noqa: E501
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    if not model_id in supported_models:
        return Error("model not available")
    return model_id_to_model(model_id)


def list_endpoints(model_id=None):  # noqa: E501
    list_model_id=[ model_id ] if model_id in supported_models else supported_models 

    return [model_id_to_endpoint(model_id) for model_id in list_model_id]

def list_models():  # noqa: E501
    """List Models

    Returns the list of ML Models. # noqa: E501


    :rtype: Models
    """
    return [model_id_to_model(model_id) for model_id in supported_models]
