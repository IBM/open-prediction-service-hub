from urllib.parse import unquote, unquote_plus
import connexion
import six
import logging

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.prediction import Prediction  # noqa: E501
from openapi_server.models.prediction_response import PredictionResponse  # noqa: E501
from openapi_server import util
from openapi_server.controllers.helper import supported_models, get_model_conf, model_decode
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
            return Error("endpoint is not available")
        # noqa: E501
        input_schema=get_model_conf(model_id)["model"]["input_schema"]
        input_args=[field["name"] for field in input_schema]
        prediction_args=[parameter.value for parameter in prediction.parameters if parameter.name in input_args]
        model_dir = model_decode(model_id)
        # TODO: loading should only be done once
        model = pickle.load(open(f"data/{model_dir}/model.pkl", "rb"))

        try:
            prediction = model.predict([prediction_args])[0]
            if not hasattr(model, 'predict_proba'):
                return {"result": {"prediction": prediction }}
            else:
                scores = model.predict_proba([prediction_args])[0].tolist()
                return {"result": {"prediction": prediction, "scores": scores}}
        except Exception as e:
            logging.warning(input_schema)
            logging.warning(input_args)
            logging.warning(prediction_args)
            logging.error(e)
            return Error(error=e.__str__)

    return Error("Cannot parse request")
