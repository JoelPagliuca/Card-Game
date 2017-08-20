PYTHON := python
PIP := pip

test:
	${PYTHON} -m unittest discover

nose:
	nosetests tests

coverage:
	nosetests tests --with-coverage --cover-erase --cover-branches --cover-inclusive --cover-html --cover-html-dir=build/htmlcov

clean:
	rm -f **/*.pyc
	rm -f *.pyc

clobber: clean
	rm -rf build
