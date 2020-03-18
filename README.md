# Decision automation on machine learning

This repository includes sample material to show how IBM Decision Services can leverage ML predictive models hosted as micro services.

The technical proposal fits with a concept of operations based on 3 main roles and 4 steps:
 - Step 1: A Data scientist elaborates an ML model in a data science tool.
 - Step 2: A Data scientist exports an ML model serialized in pickle of joblib.
 - Step 3: A developer takes the serialized ML model and hosts it as a microservice
 - Step 4: A Business user creates a decision service in IBM Digital Business Automation that invokes the hosted ML model
 

The technologies selected here to fullfill a lightweight machine learning predictive model hosting are:
- Docker, as a container standard, used here to easily build and deploy a Python environment,
- Python, the de facto prefered language for ML,
- Fastapi, the framework bringing web app and RESTfull APIs,
- Pickle, the standard serialization library for Python,


## Clone the project 
```shell script
git clone --recurse-submodules git@github.ibm.com:dba/ads-ml-service.git ads-ml-service
```
the `--recurse-submodules` option is needed to download training data for example models

## Build the ML microservice
```shell script
make image
```

## Run the ML microservice
```shell script
make launch
```
Your predictive service is ready to predict on the 127.0.0.1:8080 port.

## Usage

### Configuration example for miniloan classification

```json
{
  "name": "miniloan-lr-RandomizedSearchCV",
  "version": "v0",
  "library": "scikit-learn",
  "method_name": "predict",
  "input_schema": [
    {
      "name": "creditScore",
      "order": 0,
      "type": "float64"
    },
    {
      "name": "income",
      "order": 1,
      "type": "float64"
    },
    {
      "name": "loanAmount",
      "order": 2,
      "type": "float64"
    },
    {
      "name": "monthDuration",
      "order": 3,
      "type": "float64"
    },
    {
      "name": "rate",
      "order": 4,
      "type": "float64"
    }
  ],
  "output_schema": null,
  "metadata": {
    "name": "Loan payment classification",
    "date": "2020-03-17 13:25:23",
    "metrics": {
      "accuracy": 0.9471577261809447
    }
  }
}
```

A ML model is uniquely identified by its `name` and `version`. 

`library` will be used in next iteration (It is ignored in current version).

A ML model is a python class. The local provider needs to know the `method_name` of prediction method.

`input_schema` is used as lookup table which local provider use to find type/position of 
each feature. `type` needs to be a type in `numpy`module.

`output_schema` will be used in next iteration for parametric output mapping. It is ignored 
in the current iteration and local provider gives formatted result for the most common use 
cases (by using pre-configured output mapping).
Now the local provider supports the default output of predict/predict_proba for scikit-learn.

There is no constraint for `metadata`.

### Example for model invocation

```json
{
  "model_name": "miniloan-rfc-RandomizedSearchCV",
  "model_version": "v0",
  "params": {
    "creditScore": 5.9,
    "income": 3.0,
    "loanAmount": 5.1,
    "monthDuration": 1.8,
    "rate": 1.8
  }
}
```


