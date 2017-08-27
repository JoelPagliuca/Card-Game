.PHONY: test clean install

PYTHON := venv/bin/python
PIP := venv/bin/pip
TEST_DIR := test
TEST_RUNNER := venv/bin/nosetests

test:
	${TEST_RUNNER}

environment:
	virtualenv --no-site-packages venv

install: requirements.txt
	${PIP} install -r $<

dev: environment install

clean:
	rm -f **/*.pyc
	rm -f *.pyc
	rm -f .coverage
	rm -f .noseids

clobber: clean
	rm -rf build
	rm -rf venv