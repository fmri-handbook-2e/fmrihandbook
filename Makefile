DOCKER_IMG=fmrihandbook

docker-build:
	docker build -t ${DOCKER_IMG} .

install:
	pip install -U .
