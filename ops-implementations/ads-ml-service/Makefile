default: build

# Prepare interface schema generation
prepare-schemas-gen:
	cp ../../open-prediction-service.yaml app/gen/tmp.schemas.ops.yaml

# Build docker container
build:
    # docker buildx create --use
	rm "${CURDIR}/app/gen/tmp.schemas.ops.yaml"
	cp -f "${CURDIR}/../../open-prediction-service.yaml" "${CURDIR}/app/gen/tmp.schemas.ops.yaml"
	docker buildx build --platform linux/amd64 -t ads-ml-service:latest .

build-arm:
    # docker buildx create --use
	rm "${CURDIR}/app/gen/tmp.schemas.ops.yaml"
	cp -f "${CURDIR}/../../open-prediction-service.yaml" "${CURDIR}/app/gen/tmp.schemas.ops.yaml"
	docker buildx build --load --platform linux/arm64 -t ads-ml-service-arm64:latest .

# Launch a testing server
launch: build
	docker run --rm --read-only -it -p 127.0.0.1:8080:8080 --name ads-ml-service -e DEBUG=True ads-ml-service:latest

launch-arm:
	# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker run --rm --read-only -it -p 127.0.0.1:8080:8080 --name ads-ml-service-arm64 -e DEBUG=True ads-ml-service:latest

# Test
test: build
	docker run --rm -it --entrypoint="python3" -e RETRAIN_MODELS=1 ads-ml-service -m pytest -v app/tests

debug: build
	docker run --rm -it --entrypoint="bash" --user root ads-ml-service

test_upload:
	curl localhost:8080/upload \
	  -F "file=@$(pwd)/examples/model_training_and_deployment/ads-samples/model.pmml" \
	  --trace-ascii /dev/stdout
