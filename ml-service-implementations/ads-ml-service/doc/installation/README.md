# Installation

OPS is a containerized service. Installation consist of two steps: 
1. Build image from source code. (Register image to image registry)
2. Create services using registered/local image

## Build image

Build the image in 3 lines:
```shell script
# Clone the project
git clone git@github.ibm.com:dba/automation-decision-services-extensions.git automation-decision-services-extensions

# Build image
cd automation-decision-services-extensions/open-prediction-service/ml-service-implementations/ads-ml-service
docker build -t open-prediction:0.1.0 -t open-prediction:latest -f Dockerfile .
```
The image is then built and can be identified by two tags: `0.1.0` and `latest`. 

## Create service
