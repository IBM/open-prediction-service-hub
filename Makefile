image_dev:
	docker build -t op_dev -f docker/Dockerfile .

launch:
	docker run --rm -it -p 8080:8080 --name open-prediction op_dev

example:
	python3 src/main/python/tests/prepare_models.py

coverage:
	python3 -m pytest --cov=dynamic_hosting src/main/python/tests

lucast:
	python3 -m locust -f src/main/python/stress_test/locustfile.py


# Container Image management
IMAGE_REPO=mldecisions
IMAGE_NAME=mlservice
IMAGE_TAG=latest

ibm_register_image:
	ibmcloud cr image-rm us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} || echo "Not need to delete image"
	ibmcloud cr build -t us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} -f docker/Dockerfile .

tag_image:
	docker tag lml us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

push_to_ibm:
	docker push us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG}


# Kubernetes
KUB_CLUSTER_NAME=MicroMLService
KUB_SERVICE_NAME=mlservice
KUB_DEPLOYMENT_NAME=mlservice-deployment

get_cluster:
	ibmcloud ks workers --cluster ${KUB_CLUSTER_NAME}

get_services:
	kubectl get services

kub_clean:
	kubectl delete service ${KUB_SERVICE_NAME}
	kubectl delete deployment ${KUB_DEPLOYMENT_NAME}

kub_deploy:
	cat docker/deployment.yaml \
		| sed \
			-e "s/{{KUB_DEPLOYMENT_NAME}}/${KUB_DEPLOYMENT_NAME}/g" \
			-e "s/{{IMAGE_REPO}}/${IMAGE_REPO}/g" \
			-e "s/{{IMAGE_NAME}}/${IMAGE_NAME}/g" \
			-e "s/{{IMAGE_TAG}}/${IMAGE_TAG}/g" \
		| kubectl apply -f -

kub_service:
		cat docker/service.yaml \
		| sed \
			-e "s/{{KUB_SERVICE_NAME}}/${KUB_SERVICE_NAME}/g" \
		| kubectl apply -f -

kub: ibm_register_image kub_clean kub_deploy kub_service
	echo "Service ready"
