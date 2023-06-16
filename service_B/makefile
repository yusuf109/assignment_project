.PHONY: run

run: build
	docker run -p 5000:80 audio_process_microservice

build:
	@if ! docker image inspect audio_process_microservice >/dev/null 2>&1 ; then \
		docker build -t audio_process_microservice . ; \
	fi
