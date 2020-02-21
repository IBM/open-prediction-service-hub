image:
	docker build -t lml .

run-image:
	docker run --rm -it -p 5000:5000 --name lml lml