# generate models
schemas-gen:
	datamodel-codegen \
		--input ../../open-prediction-service.yaml \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/schemas/ops_schemas.py

# Example service
build: schemas-gen
	docker build -t ads-ml-service .

# Launch a testing server
launch: build
	docker run --rm -it -p 8080:8080 --name ads-ml-service ads-ml-service

# Test
test: build
	docker run --rm -it --entrypoint="python3" ads-ml-service -m pytest -v /app/app/tests

# Launch stress test server
locust:
	python3 -m locust -f scripts/locustfile.py
