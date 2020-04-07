image:
	docker build -t lml .

launch:
	docker run --rm -it -p 8080:8080 --name lml lml

example:
	bash  src/main/python/dynamic_hosting/example_model_training/train.sh
