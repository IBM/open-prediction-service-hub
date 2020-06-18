# Example service
default:
	docker build -t ml-service .

launch: default
	docker run --rm -it -p 8080:8080 --name ml-service ml-service


# Test
test:
	python3 -m pytest --cov=src src/tests

locust:
	python3 -m locust -f tests/stress_test/locustfile.py
