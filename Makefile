.PHONY: deps-pipenv

clean:
	rm -rf node_modules temp

HAS_PIPENV := $(shell command -v pipenv;)
deps-pipenv:
ifndef HAS_PIPENV
	pip install pipenv
endif

Pipfile.lock: Pipfile deps-pipenv
	pipenv lock

temp/make-targets/deps: Pipfile Pipfile.lock
	pipenv sync --dev
	mkdir -p temp/make-targets
	touch temp/make-targets/deps

deps: temp/make-targets/deps

temp/make-targets/js-deps: package.json yarn.lock
	yarn install
	mkdir -p temp/make-targets
	touch temp/make-targets/js-deps

js-deps: temp/make-targets/js-deps

TEST_SOURCES := $(shell find $$PWD -name '*_test.py')
test-units: $(TEST_SOURCES) deps
	pipenv run python -m unittest $(TEST_SOURCES)

# test-features: deps
# 	pipenv run behave

test: test-units

lint-python: deps
	pipenv run pylint \
		--disable duplicate-code,line-too-long,missing-module-docstring,missing-class-docstring,missing-function-docstring\
		--extension-pkg-whitelist='pydantic'\
		*.py image_sources

JAVASCRIPT_SOURCES := $(shell find $$PWD/static -name '*.js')
lint-js: $(JAVASCRIPT_SOURCES) js-deps
	yarn run eslint static

lint: lint-python lint-js

test-all: lint lint-js test

# Misc targets
ssh:
	ssh pi@eink-radiator.local

set-pipeline:
	fly -t wallhouse set-pipeline --pipeline eink-radiator --config ci/pipeline.yaml --load-vars-from ../secrets/pipeline-creds.json
