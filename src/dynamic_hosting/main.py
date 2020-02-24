#!flask/bin/python
from os import path
from flask import Flask, jsonify
from flask import request, jsonify
from flask_restx import Api, Resource, fields
from flask_restx import reqparse

import pandas as pd
from joblib import load
import pickle

import json
import requests

#
# Model registering
#


APP_ROOT = path.dirname(path.abspath(__file__))


modelDictionary = dict({
    'models': [
        {
            'path': path.join(APP_ROOT, "models/miniloandefault-rfc.joblib"),
        },
        {
            'path': path.join(APP_ROOT, "models/miniloandefault-svm.joblib"),
        },
        {
            'path': path.join(APP_ROOT, "models/iris-svc.joblib"),
        }
    ]
})

#todo
#Propagate the joblib metadata into the model management dictionary

#
# Flask
#

app = Flask(__name__)
api = Api(app)

ns = api.namespace('automation/api/v1.0/prediction/admin', description='administration')


@ns.route('/isAlive')  # Create a URL route to this resource
class HeartBeat(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        return {'answer': 'ok'}


@ns.route("/models")
class Model(Resource):
    def get(self):
        """Returns the list of ML models."""
        return modelDictionary

ns = api.namespace('automation/api/v1.0/prediction/generic', description='run any ML models')

modelInvocation = api.model('Name Model', {'name': fields.String(required = True, description="Name of the model", help="Name cannot be blank.")})

@ns.route('/')
class PredictionService(Resource):
    @api.expect(modelInvocation)
    @api.response(201, 'Category successfully created.')
    def post(self):
        """Computes a new prediction."""

        try:
            jsonDictionary = request.json
            print(jsonDictionary)

            # Model
            jsonModelDictionary = jsonDictionary["model"]
            modelName = jsonModelDictionary["name"]
            modelVersion = jsonModelDictionary["version"]
            modelFormat = jsonModelDictionary["format"]

            # Features
            jsonPayloadDictionary = jsonDictionary["features"]

            # Compose the model path
            modelPath = 'models/' + modelName + '.' + 'joblib'  # Picking joblib file by default

            # Remote read
            # response = requests.get('https://github.com/ODMDev/decisions-on-ml/blob/master/docker-python-flask-sklearn-joblist-json/models/miniloandefault-rfc.joblib?raw=true')

            # Local read
            dictionary = load(modelPath)

            # Access to the model metadata
            metadataDictionary = dictionary["metadata"]

            # Introspect the signature
            signatureParameters = metadataDictionary["signature"]
            parameterValues = []
            for parameter in signatureParameters:
                print(parameter)
                name = parameter["name"]
                type = parameter["type"]
                value = float(jsonPayloadDictionary[name])
                parameterValues.append(value)

            # Local read
            loaded_model = dictionary['model']

            # Invocation
            invocationMethod = metadataDictionary["invocation"]
            predictedClass = -1
            predictionWrapper = 0

            responseDictionary = {
                "modelPath": modelPath,
                "id": "123"
            }

            if invocationMethod == 'predict':
                predictedClass = loaded_model.predict(
                    [parameterValues])
                # Assume an array of a single element to be cast in int
                foundClass = predictedClass[0]
                responseDictionary['prediction'] = foundClass.item()  # cast into int

            if invocationMethod == 'predict_proba':
                predictionWrapper = loaded_model.predict_proba(
                    [parameterValues])

                prediction = predictionWrapper[0]

                # Needs to be generalized
                probabilities = {
                    "0": prediction[0],
                    "1": prediction[1]
                }

                responseDictionary["probabilities"] = probabilities

            # json_string = json.dumps(responseDictionary, indent=4)

            # print(responseDictionary)

            return responseDictionary

        except:
            return "KO"


if __name__ == '__main__':
    # Start a development server
    app.run(host='127.0.0.1', port=5000, debug=True)
