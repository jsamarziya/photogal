.PHONY: clean dist doctest envclean init run test

PYTHON = python3

init:
	$(PYTHON) -m venv venv
	venv/bin/pip install wheel pytest assertpy
	venv/bin/pip install -e .

run:
	FLASK_APP=photogal \
	FLASK_DEBUG=1 \
	venv/bin/flask run

test: doctest

doctest:
	venv/bin/pytest --doctest-modules --pyargs photogal

dist: test
	venv/bin/python setup.py bdist_wheel

clean:
	rm -rf build dist

envclean: clean
	rm -rf venv photogal.egg-info

