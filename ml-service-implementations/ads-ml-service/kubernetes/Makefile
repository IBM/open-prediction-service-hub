
# Register imgge
ibm_register_image:
	ibmcloud cr image-rm us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} || echo "Not need to delete image"
	ibmcloud cr build -t us.icr.io/${IMAGE_REPO}/${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile .


# Deploy service
kub_deploy:
	cat deployment.yaml \
		| sed \
  			-e "s/{{IMAGE_URL}}/us.icr.io\/{{IMAGE_REPO}}\/{{IMAGE_NAME}}:{{IMAGE_TAG}}/g" \
		| sed \
			-e "s/{{IMAGE_REPO}}/${IMAGE_REPO}/g" \
			-e "s/{{IMAGE_NAME}}/${IMAGE_NAME}/g" \
			-e "s/{{IMAGE_TAG}}/${IMAGE_TAG}/g" \
		| kubectl apply -f -

kub_service:
		kubectl apply -f service.yaml

kub: ibm_register_image kub_deploy kub_service
	echo "Service ready"
