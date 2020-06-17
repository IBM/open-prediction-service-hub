# Example service
image:
	docker build -t open-prediction-service

launch:
	docker run --rm -it -p 8080:8080 --name open-prediction-service open-prediction-service


# Test
test:
	python3 -m pytest --cov=src tests

locust:
	python3 -m locust -f tests/stress_test/locustfile.py
