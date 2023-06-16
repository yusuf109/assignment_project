.PHONY: build run clean

build:
	@cd service_A && docker build -t service_a .
	@cd service_B && docker build -t service_b .

run: build
	@docker network create my_network || true
	@docker run -d --name service_a --network=my_network -p 8000:8000 service_a
	@docker run -d --name service_b --network=my_network -p 5000:5000 service_b

clean:
	@docker stop service_a || true
	@docker stop service_b || true
	@docker rm service_a || true
	@docker rm service_b || true
	@docker network rm my_network || true
