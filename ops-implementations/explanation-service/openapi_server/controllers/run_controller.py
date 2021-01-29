import numpy as np
from openapi_server.loan_scoring import predict_proba
from openapi_server.explanations import explain
from openapi_server.common import is_flat_explanation, get_explanation_name


def prediction(body):  # noqa: E501
    """Call Prediction of specified Endpoint

     # noqa: E501

    :param prediction:
    :type prediction: dict | bytes

    :rtype: PredictionResponse
    """
    deployment_link = body['target'][0]['href']
    index = deployment_link.rfind('/')
    flat_explanation = is_flat_explanation(deployment_link[index+1:])
    # print(body['parameters'])
    buffer = np.array([item['value'] for item in body['parameters']])
    matrix = np.ndarray((buffer.shape[0],), dtype=float, buffer=buffer)
    data = matrix.reshape(1, -1)
    probability = predict_proba(data).tolist()
    no_payment_default_probability = probability[0]
    result = dict(
        result=dict(
            predicted_paymentDefault=1-round(no_payment_default_probability),
            probability_0=no_payment_default_probability,
            probability_1=probability[1]
        )
    )
    explanations = explain(matrix)
    # print(explanations)
    if flat_explanation:
        for (feature, value) in explanations:
            result['result'][get_explanation_name(feature)] = value
    else:
        result['result']['explanation'] = dict(
            (name, value) for (name, value) in explanations
        )
    # print(result)
    return result
