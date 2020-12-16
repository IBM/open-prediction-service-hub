# Open Prediction Service Java Client SDK

This folder includes:

- A ready to use Java API to invoke the OPS ML service,
- The recipe to generate a new SDK with open-api-generator based on the OpenApi description of the Open Prediction Service.

## Requirements

- Java 8
- maven

## Build and install

`# mvn clean install`

Integration tests are run against a locally started [OPS implementation](../ops-implementation/sklearn-service) listening on `http://localhost:8080`:

You can start it like this

```
> cd ../ops-implementation/sklearn-service
> docker build -t sklearn-service .
> docker run -p 8080:8080 sklearn-service
```
