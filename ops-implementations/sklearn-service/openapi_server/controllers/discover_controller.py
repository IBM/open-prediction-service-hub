import logging
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
    endpoint_parameters = get_model_conf(model_id)["endpoint"]
    links = [Link('self', f"{request.url_root}endpoints/{model_id}"),
             Link('model', f"{request.url_root}models/{model_id}")]
    return Endpoint(links=links, id=model_id, **endpoint_parameters)


def model_id_to_model(model_id):
    model_parameters = get_model_conf(model_id)["model"]
    links = [Link('self', f"{request.url_root}models/{model_id}"),
             Link('endpoint', f"{request.url_root}endpoints/{model_id}")]
    return Model(links=links, id=model_id, **model_parameters)


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


def list_endpoints(model_id=None, limit=None, offset=None, total_count=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str
    :param limit: The numbers of items to return
    :type limit: int
    :param offset: The number of items to skip before starting to collect the result set
    :type offset: int
    :param total_count: Compute total number of item
    :type total_count: bool

    :rtype: Endpoints
    """
    listed = supported_models if model_id is None or model_id not in supported_models else [model_id]
    count = 0 if not total_count else len(listed)
    start = offset if offset < len(listed) else len(listed)
    end = offset + limit if offset + limit < len(listed) else len(listed)
    filtered = listed[start:end]
    endpoints = [model_id_to_endpoint(model_id) for model_id in filtered]
    return Endpoints(endpoints=endpoints, total_count=count)


def list_models(limit=None, offset=None, total_count=None):  # noqa: E501
    """List Models

    Returns the list of ML Models. # noqa: E501

    :param limit: The numbers of items to return
    :type limit: int
    :param offset: The number of items to skip before starting to collect the result set
    :type offset: int
    :param total_count: Compute total number of item
    :type total_count: bool

    :rtype: Models
    """
    count = 0 if not total_count else len(supported_models)
    start = offset if offset < len(supported_models) else len(supported_models)
    end = offset + limit if offset + limit < len(supported_models) else len(supported_models)
    filtered = supported_models[start:end]
    models = [model_id_to_model(model_id) for model_id in filtered]
    return Models(models=models, total_count=count)
