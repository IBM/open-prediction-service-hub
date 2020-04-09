image:
	docker build -t lml .

launch:
	docker run --rm -it -p 8080:8080 --name lml lml

example:
	bash  src/main/python/dynamic_hosting/example_model_training/train.sh


# Container Image management
IMAGE_REPO=mldecisions
IMAGE_NAME=mlservice
IMAGE_TAG=latest

ibm_register_image:
	ibmcloud cr image-rm us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
	ibmcloud cr build -t us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} .

tag_image:
	docker tag lml us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

push_to_ibm:
	docker push us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}


# Kubernetes
KUB_CLUSTER_NAME=MicroMLService
KUB_SERVICE_NAME=mlservice
KUB_DEPLOYMENT_NAME=mlservice-deployment

get_servers:
	ibmcloud ks workers --cluster ${KUB_CLUSTER_NAME}

get_services:
	kubectl get services

kub_clean:
	kubectl delete service ${KUB_SERVICE_NAME}
	kubectl delete deployment ${KUB_DEPLOYMENT_NAME}

kub_deploy:
	kubectl run ${KUB_DEPLOYMENT_NAME} --image=us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} --image-pull-policy Always

kub_service:
	kubectl expose deployment/${KUB_DEPLOYMENT_NAME} --type=NodePort --name=${KUB_SERVICE_NAME} --target-port=8080 --port 8080

kub: ibm_register_image kub_clean kub_deploy kub_service
	echo "Service ready"
