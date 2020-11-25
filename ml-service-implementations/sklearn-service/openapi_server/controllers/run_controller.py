import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.prediction import Prediction  # noqa: E501
from openapi_server.models.prediction_response import PredictionResponse  # noqa: E501
from openapi_server import util
from openapi_server.controllers.helper import supported_models, get_model_conf
import pickle

def prediction(body):  # noqa: E501
    """Call Prediction of specified Endpoint

     # noqa: E501

    :param prediction: 
    :type prediction: dict | bytes

    :rtype: PredictionResponse
    """
    if connexion.request.is_json:
        prediction = Prediction.from_dict(connexion.request.get_json())
        model_id=prediction.target[0].href.split("endpoints/")[1]
        if not model_id in supported_models:
            return Error("model is not availale")
        # noqa: E501
        input_schema=get_model_conf(model_id)["model"]["input_schema"]
        input_args=[field["name"] for field in input_schema]
        prediction_args=[parameter.value for parameter in prediction.parameters if parameter.name in input_args]
        model=pickle.load(open(f"data/{model_id}/model.pkl","rb")) #TODO: loading should only be done once
        prediction=model.predict([prediction_args])[0]
        return {"output_schema": {"predictions": prediction }}
    return Error("Cannot parse request")
