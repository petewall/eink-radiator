build:
	docker build --tag petewall/eink-radiator .

push:
	docker push petewall/eink-radiator

test: lint

lint:
	pipenv run pylint *.py image_sources

ssh:
	ssh pi@eink-radiator.local
