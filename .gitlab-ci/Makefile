VERSION=$(shell date --iso)

all:
	./run-docker.sh build  --base ci-checks --version 0.0.$(VERSION)

push:
	./run-docker.sh push  --base ci-checks --version 0.0.$(VERSION)
