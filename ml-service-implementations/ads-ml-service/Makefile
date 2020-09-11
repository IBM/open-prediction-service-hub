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
schemas-gen:
	datamodel-codegen \
		--input ../../open-prediction-service.yaml \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/schemas/ops_schemas.py
