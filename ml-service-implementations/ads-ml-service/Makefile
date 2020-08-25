# Example service
default:
	docker build -t ads-ml-service .

launch: default
	docker run --rm -it -p 8080:8080 --name ads-ml-service ads-ml-service

# Test
test:
	python3 -m pytest --cov=src src/tests

locust:
	python3 -m locust -f scripts/locustfile.py

# generate models
model-gen:
	datamodel-codegen \
		--input ../../open-prediction-service.json \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/model/ops_model.py
