
from openapi_server.models.link import Link
from openapi_server.models.model import Model  # noqa: E501
from openapi_server.models.models import Models  # noqa: E501
from openapi_server.models.endpoint import Endpoint  # noqa: E501
from openapi_server.models.endpoints import Endpoints  # noqa: E501
from openapi_server.common import is_flat_explanation, get_explanation_name  # noqa: E501
from flask import request

FEATURES = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement']


def get_input_schema():
    return [dict(name=feature, type='float', order=index+1) for (index, feature) in enumerate(FEATURES)]


def get_output_schema(flat_explanation):
    output_schema = dict(
        predicted_paymentDefault=dict(type='int'),
        probability_0=dict(type='float'),
        probability_1=dict(type='float')
    )
    if flat_explanation:
        for feature in FEATURES:
            output_schema[get_explanation_name(feature)] = dict(type='float')
    else:
        output_schema['explanation'] = dict(
            type='object',
            fields=[dict(name=f'{feature}', type='float') for feature in FEATURES]
        )
    return output_schema


def get_endpoint(model_id):
    endpoint = Endpoint(
        links=[
            Link('self', f'{request.url_root}endpoints/{model_id}'),
            Link('model', f'{request.url_root}models/{model_id}')
        ],
        id=model_id,
        name='Deployment for payment default prediction with flat explanation'
        if is_flat_explanation(model_id)
        else 'Deployment for payment default prediction with explanation as object',
        deployed_at='2020-10-01T14:44:27.498Z',
        status='in_service'
    )
    return endpoint


def get_model(model_id):
    flat_explanation = is_flat_explanation(model_id)
    model = Model(
        links=[
            Link('endpoint', f'{request.url_root}endpoints/{model_id}'),
            Link('self', f'{request.url_root}models/{model_id}')
        ],
        id=model_id,
        input_schema=get_input_schema(),
        created_at='2020-10-14T13:49:15.257Z',
        name='Model for payment default prediction with flat explanation'
        if flat_explanation
        else 'Model for payment default prediction with explanation as object',
        modified_at='2020-10-01T14:44:27.498Z',
        output_schema=get_output_schema(flat_explanation)
    )
    return model


def get_endpoint_by_id(endpoint_id):
    """Get an Endpoint

    Returns an ML Endpoint. # noqa: E501

    :param endpoint_id: ID of endpoint
    :type endpoint_id: str

    :rtype: Endpoint
    """
    return get_endpoint(endpoint_id)


def get_model_by_id(model_id):
    """Get a Model

    Returns a ML model. # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Model
    """
    return get_model(model_id)


def list_endpoints(model_id=None):  # noqa: E501
    """List Endpoints

     # noqa: E501

    :param model_id: ID of model
    :type model_id: str

    :rtype: Endpoints
    """
    return Endpoints(
        endpoints=[get_endpoint(model_id)]
        if model_id
        else [get_endpoint("1"), get_endpoint("2")]
    )


def list_models():  # noqa: E501
    """List Models

    Returns the list of ML Models. # noqa: E501


    :rtype: Models
    """
    return Models(models=[get_model("1"), get_model("2")])
