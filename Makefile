# HAS_GINKGO := $(shell command -v ginkgo;)
HAS_GOLANGCI_LINT := $(shell command -v golangci-lint;)
# HAS_COUNTERFEITER := $(shell command -v counterfeiter;)
PLATFORM := $(shell uname -s)

# #### DEPS ####
# .PHONY: deps-go-binary deps-counterfeiter deps-golangci-lint deps-modules

# deps-counterfeiter: deps-go-binary
# ifndef HAS_COUNTERFEITER
# 	go install github.com/maxbrunsfeld/counterfeiter/v6@latest
# endif

# deps-ginkgo: deps-go-binary
# ifndef HAS_GINKGO
# 	go install github.com/onsi/ginkgo/ginkgo@latest
# endif

deps-modules:
	go mod download

# #### SRC ####
# lib/libfakes/fake_firmware_store.go: lib/firmware_store.go
# 	go generate lib/firmware_store.go

# #### TEST ####
.PHONY: lint

lint:
ifndef HAS_GOLANGCI_LINT
ifeq ($(PLATFORM), Darwin)
	brew install golangci-lint
endif
ifeq ($(PLATFORM), Linux)
	curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin
endif
endif
	golangci-lint run

# test: lib/libfakes/fake_firmware_store.go deps-modules deps-ginkgo
# 	ginkgo -r -skipPackage test .

# integration-test: deps-modules deps-ginkgo
# 	ginkgo -r test/integration

# test-all: lib/libfakes/fake_dbinterface.go deps-modules deps-ginkgo
# 	ginkgo -r .

# #### BUILD ####
.PHONY: build
SOURCES = $(shell find . -name "*.go" | grep -v "_test\." )

build/eink-radiator: $(SOURCES) deps-modules
	go build -o build/eink-radiator github.com/petewall/eink-radiator/v2

build: build/eink-radiator

run: build/eink-radiator
	build/eink-radiator

# #### DEVOPS ####
ci/pipeline.yaml: ci/pipeline-template.yaml ci/data.yaml
	ytt --file ci/pipeline-template.yaml --file ci/data.yaml > ci/pipeline.yaml

set-pipeline: ci/pipeline.yaml
	fly --target wallhouse set-pipeline \
		--pipeline eink-radiator \
		--config ci/pipeline.yaml
