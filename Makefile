.PHONY: clean dist doctest envclean init pytest run test

PYTHON = python3

init:
	$(PYTHON) -m venv venv
	venv/bin/pip install wheel pytest assertpy
	venv/bin/pip install -e .

run:
	FLASK_APP=photogal \
	FLASK_DEBUG=1 \
	venv/bin/flask run

test: doctest pytest

doctest:
	venv/bin/pytest --doctest-modules --pyargs photogal

pytest:
	venv/bin/pytest

dist: test
	venv/bin/python setup.py bdist_wheel

clean:
	rm -rf build dist

envclean: clean
	rm -rf venv src/photogal.egg-info .pytest_cache

