build:
	docker build --tag petewall/eink-radiator .

push:
	docker push petewall/eink-radiator

ssh:
	ssh pi@eink-radiator.local