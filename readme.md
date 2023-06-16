## How to run both microservices?

Process-1: Docker
1) cd assignment_project/service_A
2) run: make run
3) cd assignment_project/service_B
4) run: make run

N.B: Can globally run both services using command: make run
Can stop/clear all the running containers using: make clear
Make sure you're in the project root folder(assignment_project/)
Running both serives well but had an network issue to call service_B API


Process-2: Virtualenv
1) create a virtualenv outside of the project: virtualenv venv
2) activate it: venv/bin/activate
3) cd serice_A & run: pip install -r service_A/requirements.txt
4) run: python app/main.py
4) cd serice_B & run: pip install -r service_B/requirements.txt
5) run: python app/main.py


## API's:
http://localhost:4000/process_audio


Lost time:
Running both services using docker and makefile
Had an docket network issue and couldn't solve that
Killed a lots of time


Architecture:
Tried to keep the architecture as simple as possible
Only 2 main.py module is enough for this small microservices

What could do better?
Writing proper docstring, typing
Proper unit tests
