PROJECT=vipe
MY_CURR_DIR=$(shell pwd)
MY_PYTHON_PATH=$(shell echo ${PYTHONPATH})

all: build-source-package

build-source-package: clean rst-description-file
	./setup.py sdist

install-user: clean rst-description-file
	./setup.py install --user

install: clean rst-description-file
	sudo ./setup.py install

uninstall-user:
	pip uninstall $(PROJECT)

uninstall:
	sudo pip uninstall $(PROJECT)

test:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); nosetests -v

## Check correctness of the `.travis.yml` file
check-travis:
	travis-lint

check-package-metatada: rst-description-file
	./setup.py check --restructuredtext

html-readme:
	mkdir -p tmp
	pandoc -N -t html -s --no-wrap -o tmp/README.html README.md

clean:
	rm -rf build dist $(PROJECT).egg-info docs-api tmp

## PyPI requires the description of the package to be in the reStructuredText format.
## This is how we generate it from the Markdown README.
rst-description-file:
	mkdir -p tmp
	pandoc --from=markdown --to=rst README.md -o tmp/README.rst

## Uplading to testpypi and pypi as defined below requires two profiles to be defined 
## in the `~/.pypirc` file: `test` and `pypi`. On my computer this looks like this:
## 
## [distutils]
## index-servers=
##     pypi
##     test
## 
## [test]
## repository = https://testpypi.python.org/pypi
## username = XXXX
## password = XXXX
## 
## [pypi]
## repository = https://pypi.python.org/pypi
## username = XXXX
## password = XXXX

## Note that in order to make the `bdisk_wheel` option work you need to have
## `wheel` Python package installed.

upload-to-testpypi-and-install: rst-description-file
	./setup.py sdist bdist_wheel upload -r test
	pip install --user -i https://testpypi.python.org/pypi $(PROJECT)

upload-to-pypi: rst-description-file
	./setup.py sdist bdist_egg bdist_wheel upload -r pypi
