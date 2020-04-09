clean:
	rm -rf temp
	docker rmi petewall/eink-radiator

# Docker image targets
build:
	docker build --tag petewall/eink-radiator .

push:
	docker push petewall/eink-radiator

# Code targets
temp/make-targets/deps: Pipfile Pipfile.lock
	if ! command -v pipenv ; then pip install pipenv; fi
	pipenv sync --dev
	mkdir -p temp/make-targets
	touch temp/make-targets/deps

deps: temp/make-targets/deps

test: lint deps 
	pipenv run python -m unittest *_test.py

lint: deps
	pipenv run pylint \
		--disable missing-module-docstring,missing-class-docstring,missing-function-docstring\
		*.py image_sources

# Misc targets
ssh:
	ssh pi@eink-radiator.local
