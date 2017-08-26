.PHONY: test clean

PYTHON := python
PIP := pip
TEST_DIR := test
TEST_RUNNER := nosetests

test:
	${TEST_RUNNER}

clean:
	rm -f **/*.pyc
	rm -f *.pyc
	rm -f .coverage
	rm -f .noseids

clobber: clean
	rm -rf build
