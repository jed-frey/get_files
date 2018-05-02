# Config

# Makefile directory
MK_DIR = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

# Project name
PROJ ?= $(notdir ${MK_DIR})
# Virtual environment path
VENV ?= ${MK_DIR}
# Hostname
HOST:=$(shell hostname)
# Executable paths
PIP:=${VENV}/bin/pip
PYTHON:=${VENV}/bin/python


# Base python modules to install before everything else
# Some projects need wheel, numpy and cython
# before they will install correctly.
BASE_MODULES?=setuptools wheel numpy

# Targets
.DEFAULT: all
.PHONY: all
all:
	$(error No default target)

.PHONY: venv
venv: ${PYTHON}

${PYTHON}: requirements_dev.txt
	${MAKE} clean
	python3 -mvenv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade ${BASE_MODULES}
	${PIP} install --upgrade --requirement ${<}

.PHONY: lazy
lazy:
	autopep8 --in-place --aggressive --aggressive --aggressive get_files/*.py
	isort --apply get_files/*.py

.PHONY: lint
lint:
	@pylint --rcfile=pylint.cfg get_files

.PHONY: clean
clean:
	@echo ---- Cleaning ${PROJ} ----
	git clean -xfd
