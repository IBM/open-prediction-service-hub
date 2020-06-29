# Installation

OPS is a containerized service. Installation consist of three steps: 
1. Building an image from source code.
2. Registering image to image registry (Optional for local deployment).
3. Create-ing services using registered/local image.

## Build image

First clone the project to retrieve the files locally and then build an image.
```shell script
# Clone the project
git clone https://github.com/icp4a/automation-decision-services-extensions.git automation-decision-services-extensions

# Build image
cd automation-decision-services-extensions/open-prediction-service/ml-service-implementations/ads-ml-service
docker build -t open-prediction:0.1.0 -t open-prediction:latest -f Dockerfile .
```
The image is then built and can be identified by two tags: `0.1.0` and `latest`.

To verify, run
```shell script
docker images | grep open-prediction
```

and you will see:
![OpenApi](build_image.png)

## Register image to image registry (Optional for local deployment)

Suppose you have a docker hub account 
(e.g. username: `fake_username`, email: `fake_email@example.com`)

Images in public registry need to contain user name. Add new tags for the image.
```shell script
docker tag open-prediction:0.1.0 fake_username/open-prediction:0.1.0
docker tag open-prediction:latest fake_username/open-prediction:latest
```

To verify, run
```shell script
docker images | grep open-prediction
```

Then you will see some thing like
![OpenApi](add_new_tag.png)

Login your docker hub account
```shell script
docker login --username=fake_username --email=fake_email@example.com
```

Then you will see some thing like
```shell script
WARNING: login credentials saved in /home/username/.docker/config.json
Login Succeeded
```

Finally, push image to docker hub.
```shell script
docker push fake_username/open-prediction:0.1.0
docker push fake_username/open-prediction:latest
```

Your image is now available for non local environments.

## Create service

### 1. Local service

As you expect, simply run the image

```shell script
docker run --detach --restart=always \
  --publish 80:8080 \
  --name open-prediction \
  open-prediction:latest
```

To verify, run
```shell script
docker ps | grep open-prediction
```

Then you will see some thing like
![OpenApi](ops_docker.png)

### 2. Kubernetes cluster

This part is not designed to offer a fine tuned ops cluster in kubernetes, but
a minimum example of working ops instance.

Suppose you have a working kubernetes cluster and have configured kubectl
properly. To verify that, run `kubectl cluster-info`, your nodes should be listed.

`deployment.yaml` and `service.yaml` are available in `ads-ml-service/kubernetes`.
There is one remaining configuration to be done: `{{IMAGE_URL}}` inside `deployment.yaml` has not been configured yet.
Replace it by the image URL you got in [Register image to image registry](#register-image-to-image-registry-optional-for-local-deployment) section.

After replacing `{{IMAGE_URL}}`, apply configurations:

```shell script
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Find service address by:

```shell script
kubectl get service ads-ml-service-service
```

Then you will see some thing like
![OpenApi](get_service.png)

ads-ml-service is available at `<none>` (replace it by your cluster address) on port `30000`.
