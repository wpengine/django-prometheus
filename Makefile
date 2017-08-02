IMAGE=wpengine/microservice

build:
	@docker build . -t ${IMAGE}

test: build
	@docker run --rm -i ${IMAGE} python setup.py test

sdist: build
	@docker run -e BUILD_NUMBER --rm -t -v ${PWD}:/app ${IMAGE} python setup.py sdist

shell: build
	@docker run --rm -it -v ${PWD}:/app ${IMAGE} /bin/sh

clean:
	rm -rf dist django_prometheus.egg-info
