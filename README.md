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
