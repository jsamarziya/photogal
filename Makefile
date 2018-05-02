.PHONY: clean dist doctest envclean init pytest run test upgrade

PYTHON = python3.6

init:
	$(PYTHON) -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install assertpy pytest pytest-flask wheel
	venv/bin/pip install -e .

upgrade:
	venv/bin/pip install --upgrade --upgrade-strategy eager -e  .

run:
	FLASK_APP=photogal \
	FLASK_ENV=development \
	venv/bin/flask run

test: pytest

doctest:
	venv/bin/pytest --doctest-modules --pyargs photogal

pytest:
	venv/bin/pytest tests

dist: test
	venv/bin/python setup.py bdist_wheel

clean:
	rm -rf build dist

envclean: clean
	rm -rf venv src/photogal.egg-info .pytest_cache

