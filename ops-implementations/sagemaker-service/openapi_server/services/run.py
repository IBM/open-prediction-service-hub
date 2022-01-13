#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#

import sys

import boto3
import botocore
import numpy as np
import sagemaker.deserializers as sage_deserializers
import sagemaker.serializers as sage_serializers

import openapi_server.models as openapi_models

npy_serializer = sage_serializers.NumpySerializer()
npy_deserializer = sage_deserializers.NumpyDeserializer()


def prediction(body):  # noqa: E501
    """Call Prediction of specified deployment

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PredictionResponse
    """
    # Retrieve parameters
    req_data = []
    for param in body['parameters']:
        req_data.append(param['value'])
    data = np.array([req_data])

    # Retrieve target
    endpoint = None
    for target in body['target']:
        if 'rel' in target and target['rel'] == 'endpoint':
            endpoint = target['href']

    if not endpoint:
        return openapi_models.Error(error='endpoint should be provided in target array')

    # client.invoke_endpoint works with bytes buffers
    # serialize     input
    # deserialize   output
    # content type  The MIME type of the input data in the request body.
    [serializer, deserializer, contentType] = [npy_serializer, npy_deserializer, 'application/x-npy']

    body = serializer.serialize(data)

    try:
        client = boto3.client('sagemaker-runtime')
        # Invoke endpoint with numpy content type
        response = client.invoke_endpoint(
            EndpointName=endpoint,
            Body=body,
            ContentType=contentType
        )
        response_body = response["Body"]
        result = deserializer.deserialize(response_body, response["ContentType"])
        predictions = result[0]
        return openapi_models.PredictionResponse(result=dict(predictions=predictions))
    except botocore.exceptions.ClientError as error:
        return openapi_models.Error(error=str(error))
    except botocore.exceptions.ParamValidationError as error:
        return openapi_models.Error(error=str(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return openapi_models.Error(error=str(sys.exc_info()[0]))
