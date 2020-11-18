import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.prediction import Prediction  # noqa: E501
from openapi_server.models.prediction_response import PredictionResponse  # noqa: E501
from openapi_server import util


def prediction(prediction):  # noqa: E501
    """Call Prediction of specified Endpoint

     # noqa: E501

    :param prediction: 
    :type prediction: dict | bytes

    :rtype: PredictionResponse
    """
    if connexion.request.is_json:
        prediction = Prediction.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
