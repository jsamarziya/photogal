.PHONY: clean dist doctest envclean init test

PYTHON = python3

init:
	$(PYTHON) -m venv venv
	venv/bin/pip install wheel pytest
	venv/bin/pip install -e .

test: doctest

doctest:
	venv/bin/pytest --doctest-modules --pyargs photogal

dist: test
	venv/bin/python setup.py bdist_wheel

clean:
	rm -rf build dist

envclean: clean
	rm -rf venv photogal.egg-info
