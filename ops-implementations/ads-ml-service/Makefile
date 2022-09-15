default: build

# Prepare interface schema generation
prepare-schemas-gen:
	ln -s "../../../../open-prediction-service.yaml" "${CURDIR}/app/gen/tmp.schemas.ops.yaml"

# Build docker container
build: prepare-schemas-gen
	docker build -t ads-ml-service:latest .

# Launch a testing server
launch: build
	docker run --rm --read-only -it -p 127.0.0.1:8080:8080 --name ads-ml-service -e DEBUG=True ads-ml-service:latest

# Test
test:
	python3 -m tox

debug: build
	docker run --rm -it --entrypoint="bash" --user root ads-ml-service

test_upload:
	curl localhost:8080/upload \
	  -F "file=@${CURDIR}/examples/model_training_and_deployment/ads-samples/model.pmml" \
	  --trace-ascii /dev/stdout
