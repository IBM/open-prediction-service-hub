default: build

# Prepare interface schema generation
prepare-schemas-gen:
	cp ../../open-prediction-service.yaml app/gen/tmp.schemas.ops.yaml

# Build docker container
build: prepare-schemas-gen
	docker build -t ads-ml-service:latest .

# Launch a testing server
launch: build
	docker run --rm --read-only -it -p 8080:8080 --name ads-ml-service ads-ml-service:latest

# Test
test: build
	docker run --rm -it --entrypoint="python3" -e RETRAIN_MODELS=1 ads-ml-service -m pytest -v app/tests

debug: build
	docker run --rm --read-only -it --entrypoint="bash" --user 0 ads-ml-service

# Launch stress test server
locust:
	python3 -m locust -f scripts/locustfile.py
