# Example service
image:
	docker build -t open-prediction -f docker/Dockerfile .

launch:
	docker run --rm -it -p 8080:8080 --name open-prediction open-prediction


# Test
coverage:
	python3 -m pytest --cov=dynamic_hosting src/main/python/tests

lucast:
	python3 -m locust -f src/main/python/stress_test/locustfile.py


# Register imgge
ibm_register_image:
	ibmcloud cr image-rm us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} || echo "Not need to delete image"
	ibmcloud cr build -t us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} -f docker/Dockerfile .


# Deploy service
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

kub: ibm_register_image kub_deploy kub_service
	echo "Service ready"
