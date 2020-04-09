image:
	docker build -t lml .

launch:
	docker run --rm -it -p 8080:8080 --name lml lml

example:
	bash  src/main/python/dynamic_hosting/example_model_training/train.sh


# Kubernetes

kub_clean:
	kubectl delete service mlservice
	kubectl delete deployment mlservice-deployment

kub_deploy:
	kubectl run mlservice-deployment --image=us.icr.io/mldecisions/mlservice:latest --image-pull-policy Always

kub_service:
	kubectl expose deployment/mlservice-deployment --type=NodePort --name=mlservice --target-port=8080 --port 8080

get_servers:
	ibmcloud ks workers --cluster MicroMLService

ibm_register_image:
	ibmcloud cr build -t us.icr.io/mldecisions/mlservice:latest .

tag_image:
	docker tag lml us.icr.io/mldecisions/mlservice:latest

push_to_ibm:
	docker push us.icr.io/mldecisions/mlservice:latest

kub: ibm_register_image kub_deploy kub_service get_servers
	echo "Service ready"
