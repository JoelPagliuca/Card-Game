PYTHON := python
PIP := pip

test:
	${PYTHON} -m unittest discover

clean:
	rm -f **/*.pyc
	rm -f *.pyc