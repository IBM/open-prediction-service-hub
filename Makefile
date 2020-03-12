image:
	docker build -t lml .

run-image:
	docker run --rm -it -p 8080:8080 --name lml lml

pyclient:
	swagger-codegen generate -l python -i generated/src/main/openapi/openapi.json  -o generated/src/main/python/mlc