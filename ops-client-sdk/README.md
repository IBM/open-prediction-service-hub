# Open Prediction Service Java Client SDK

This folder includes:

- A ready to use Java API to invoke the OPS ML service,
- The recipe to generate a new SDK with open-api-generator based on the OpenApi description of the Open Prediction Service.

## Requirements

- Java 8
- maven

## Build and install

`# mvn clean install`

Integration tests are run against a locally started [OPS implementation](../ml-service) listening on `http://localhost:8080/v1`

