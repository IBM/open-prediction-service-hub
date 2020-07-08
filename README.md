# Open Prediction Service

The Open Prediction Service API is an effort to provide an Open API that enables unsupported native ML Providers in Decision Designer or Decision Runtime.

Thanks to this service, as any third party ML tools can be integrated to match the API specifications, third party ML tools can be reached out the same way for ML model discovery and invocation in Decision Designer or Decision Runtime.
The Open Prediction Service API is suitable for both ML proxy service and custom ML service which provides a lot of flexibility and different level support.

![OPS](doc/ops.png)

In this repository we provide:
- a reference implementation for [scikit-learn](https://scikit-learn.org/) and [XGBoost](https://xgboost.ai/)
- an Open Prediction Service Java Client SDK

### Reference implementation for [scikit-learn](https://scikit-learn.org/) and [XGBoost](https://xgboost.ai/)

We provide an Open Source implementation of this service based on two well known python Machine Learning SDK : [scikit-learn](https://scikit-learn.org/) and [XGBoost](https://xgboost.ai/) based on a docker container for easier deployments.

This reference implementation is called `ads-ml-service`.

Instructions to build an use are inside the [ml-service-implementations/ads-ml-service](ml-service-implementations/ads-ml-service/README.md) folder.

### Open Prediction Service Java Client SDK
We also provide a Java SDK based on the Open Prediction Service API to enable any java based application to use this Open architecture.

Instructions to build an use are inside the [ops-client-sdk](ops-client-sdk) folder.

## Open API specification

The Open Prediction Service is available as an [Open API v3 specification](open-prediction-service.json). The specification has two main sections:

- *Admin* section for describing endpoints for uploading, getting or deleting models into the the server.
- *ML* section that covers the prediction call endpoint

All the types manipulated by the different endpoints are described in the *Schemas* section below.

![OpenAPI](doc/ops-OpenApi.jpg)

### *Admin* section

#### Status `/v1/status` `GET`

![status](doc/ops-status.jpg)

This endpoint can be used to test the availability of the service. It returns the number of models it is serving.

#### Models `/v1/models`

##### Retrieve `GET` 

![ops-get-models](doc/ops-get-models.jpg)

This endpoint will return the list of the models it is serving.

##### Upload `POST`

![ops-post-models](doc/ops-post-models.jpg)

This endpoint will allow to upload a pickle file as a new serving model.

##### Remove `DELETE`

##### ![ops-delete-models](doc/ops-delete-models.jpg)

This endpoint will remove a given model.

#### *ML* section

##### Call prediction `/v1/invocations` `POST`

![ops-post-invocations](doc/ops-post-invocations.jpg)

### License
Apache License Version 2.0, January 2004.