# Decision automation on machine learning

[![Build Status](https://travis.ibm.com/dba/ads-ml-service.svg?token=1gxxdyFN2gDs6CM3JxPc&branch=dev)](https://travis.ibm.com/dba/ads-ml-service)

This repository is part of ADS project.

## Usage

To clone the project 
```shell script
git clone --recurse-submodules git@github.ibm.com:dba/ads-ml-service.git ads-ml-service
```

To build the microservice image
```shell script
docker build -t embedded_ml .
```

To test the microservice
```shell script
docker run --rm -it -p 8080:8080 --name lml embedded_ml
```
Your predictive service is then ready at `http://localhost:8080/v1` and 
its openapi docs is available at `http://localhost:8080/v1/docs`.



### Configuration example for miniloan classification

```json
{
  "name": "miniloan-rfc",
  "version": "v0",
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
  "output_schema": {
        "attributes": [
            {
                "name": "prediction",
                "type": "string"
            },
            {
                "name": "probabilities",
                "type": "[Probability]"
            }
        ]
  },
  "metadata": {
    "description": "Loan payment classification",
    "author": "Somebody",
    "trained_at": "2020-03-17 13:25:23",
    "class_names": {
      "0": "false",
      "1": "true"
    },
    "metrics": [
      {
        "name":  "accuracy",
        "value": 0.9471577261809447
      }
    ]
  }
}
```

ML model is uniquely identified by its `name` and its `version`. 

ML models are python classes. Local provider needs to know the `method_name` of prediction method.

`input_schema` is used as lookup table which local provider use to find type/position of 
each feature. `type` needs to be a type alias in `numpy`module.

`output_schema` will be used in next iteration for parametric output mapping. It is ignored 
in the current iteration and local provider gives formatted result for the most common use 
cases (by using pre-configured output mapping).
Now the local provider supports the default output of predict/predict_proba for scikit-learn.

`metadata` needs to have `description`, `trained_at`, `author` and associated `metrics`.


### Example for model invocation

Request body
```json
{
  "model_name": "miniloan-rfc",
  "model_version": "v0",
  "params": [
        {
            "name": "creditScore",
            "value": 400
        }, {
            "name": "income",
            "value": 45000
        }, {
            "name": "loanAmount",
            "value": 100000
        }, {
            "name": "monthDuration",
            "value": 24
        }, {
            "name": "rate",
            "value": 2.0
        }
    ]
}
```

`model_name` and `model_version`are used to load ml model from storage. Parameters of ml
models are arranged in key-values pairs.

Response body may looks like:
```json
{
    "prediction": "true",
    "probabilities": [
        {
          "class_name": "true",
          "class_index": "0",
          "value": 0.66
        },
        {
          "class_name": "false",
          "class_index": "0",
          "value": 0.34
        }
    ]   
}
```
when we want to determine whether accept such application. (the attribute `probabilities`
may be null)

or looks like:
```json
{
    "prediction": "534"
}
```
when we want to calculate some scores related to this application.


## Example of model creation
[here](examples/model_training/README.md)

## Features to be added

* Range support
* Add format for numerical features
