#!flask/bin/python
import os
from flask import Flask, jsonify
from flask import request, jsonify
from flask_restplus import Api, Resource
from flask_restplus import reqparse

import pandas as pd
from joblib import load
import pickle

import json
import requests

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

ns = api.namespace('automation/api/v1.0/prediction/static', description='adhoc API to run embedded models')

#@ns.route('/prediction/api/v1.0/loandefault', defaults={'creditScore':600, 'income': 100000, 'loanAmount':100000, 'monthDuration':120, 'rate':0.05,'yearlyReimursement':1000})
@ns.route('/prediction/api/v1.0/loandefault')
@api.param('yearlyReimbursement', 'The loan yearly reimbursement')
@api.param('rate', 'The loan rate')
@api.param('monthDuration', 'The loan duration in months')
@api.param('loanAmount', 'The loan amount')
@api.param('income', 'The income of the borrower')
@api.param('creditScore', 'the credit score of the borrower')
class LoanDefaultRiskScoring(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        creditScore = float(request.args.get('creditScore'))
        income = float(request.args.get('income'))
        loanAmount = float(request.args.get('loanAmount'))
        monthDuration = float(request.args.get('monthDuration'))
        rate = float(request.args.get('rate'))
        yearlyReimbursement = float(request.args.get('yearlyReimbursement'))

        modelPath = 'models/miniloandefault-rfc.pkl'
        loaded_model = pickle.load(open(modelPath, 'rb'))
        probabilities = loaded_model.predict_proba([[creditScore, income, loanAmount, monthDuration, rate, yearlyReimbursement]])

        responseDictionary = {
            "modelPath": modelPath,
            "description": "risk that loan payment default occurs",
            "probability": probabilities[0,0]
        }

        return responseDictionary
    
if __name__ == '__main__':
    # Start a development server
    app.run(port=5000,host='127.0.0.1')
