.PHONY: run

run: build
	docker run -p 8000:80 audio_microservice

build:
	@if ! docker image inspect audio_microservice >/dev/null 2>&1 ; then \
		docker build -t audio_microservice . ; \
	fi
