.PHONY: help test clean install server demo configure

PYTHON := venv/bin/python
PIP := venv/bin/pip
TEST_DIR := test
TEST_RUNNER := venv/bin/nosetests

help:		## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

test:		## Run unit tests
	${TEST_RUNNER}

demo:		## Run the manual testing setup
	${PYTHON} main.py

server:		## Run the python WebSocket server
	${PYTHON} server/app.py

environment:	## Make the virtualenv
	virtualenv --no-site-packages venv

install:	## install the requirements into the virtualenv
install: server/requirements.txt
	${PIP} install -r $<

configure: environment install		##

clean:		##
	rm -f **/*.pyc
	rm -f *.pyc
	rm -f .coverage
	rm -f .noseids

clobber:	##
clobber: clean
	rm -rf build
