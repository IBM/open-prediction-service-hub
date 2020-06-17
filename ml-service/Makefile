# Example service
image:
	docker build -t open-prediction-service

launch:
	docker run --rm -it -p 8080:8080 --name open-prediction-service open-prediction-service


# Test
coverage:
	python3 -m pytest --cov=dynamic_hosting src/main/python/tests

lucast:
	python3 -m locust -f src/main/python/stress_test/locustfile.py
