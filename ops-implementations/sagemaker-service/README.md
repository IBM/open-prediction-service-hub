# Open Prediction Service for Amazon SageMaker

This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

1. [Getting Started](#getting-started)

2. [Open Prediction Service](#open-prediction-service)

## Getting Started

### Prerequisites

Python 3.7

Docker

### Run the microservice on a Docker container

To build the microservice image

```sh
docker build -t sagemaker-service .
```

To run the microservice

```sh
docker run \
    -p 8080:8080 \
    -e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
    -e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
    -e AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> \
    --name sagemaker-service \
    sagemaker-service
```
If you want to run the microservice on another port
```sh
docker run \
    -p <PORT>:8080 \
    -e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
    -e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
    -e AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> \
    --name sagemaker-service \
    sagemaker-service
```

To check that you have a running container
```sh
docker ps -f name=sagemaker-service
```

> Your predictive service is available at [http://localhost:8080/](http://localhost:8080/).

> Swagger UI documentation is available at [http://localhost:8080/ui](http://localhost:8080/ui)

Or on the port of choice rescpectively at `http://localhost:<PORT>/` and `http://localhost:<PORT>/ui`

### Stop the microservice
To stop the container
```sh
docker stop sagemaker-service
```

### Run the microservice without Docker
```sh
pip3 install -r requirements.txt
python3 -m swagger_server
```

### Tests

__To launch unit tests, use tox:__
```
pip3 install tox
tox
```

__To launch tests on your SageMaker instance:__

First, make sure you have a working and configured environment to use AWS SDK (Option 3, 4 or 5 as described in [AWS SDK documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials))

Then, run tests using tox:
```
pip3 install tox
tox swagger_server/test
```