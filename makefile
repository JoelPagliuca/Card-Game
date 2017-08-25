.PHONY: test coverage clean

PYTHON := python
PIP := pip
TEST_DIR := test
TEST_RUNNER := nosetests

test:
	${TEST_RUNNER} ${TEST_DIR}

coverage:
	${TEST_RUNNER} ${TEST_DIR} --with-coverage --cover-erase --cover-branches --cover-inclusive --cover-html --cover-html-dir=build/htmlcov

clean:
	rm -f **/*.pyc
	rm -f *.pyc

clobber: clean
	rm -rf build
