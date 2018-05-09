.PHONY: clean clean_all clean_db clean_env clean_images clean_instance dist doctest init pytest run test upgrade

PYTHON = python3.6
ROOT_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

init:
	$(PYTHON) -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install assertpy pytest pytest-flask pytest-datadir wheel
	venv/bin/pip install -e .

upgrade:
	venv/bin/pip install --upgrade --upgrade-strategy eager -e  .

run:
	FLASK_APP=photogal \
	FLASK_ENV=development \
	FLASK_INSTANCE_PATH="$(ROOT_DIR)instance" \
	venv/bin/flask run

test: pytest

doctest:
	venv/bin/pytest --doctest-modules --pyargs photogal

pytest:
	venv/bin/pytest tests

dist: test
	venv/bin/python setup.py bdist_wheel

clean:
	rm -rf build dist .pytest_cache

clean_db:
	rm -f instance/photogal.db

clean_images:
	rm -rf instance/images

clean_instance: clean_db clean_images

clean_env:
	rm -rf venv src/photogal.egg-info

clean_all: clean clean_env clean_instance
