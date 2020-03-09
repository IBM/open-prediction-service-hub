image:
	docker build -t lml .

run-image:
	docker run --rm -it -p 8080:8080 --name lml lml