PROJECT=vipe
MY_CURR_DIR=$(shell pwd)
MY_PYTHON_PATH=$(shell echo ${PYTHONPATH})
PIP=pip3

all: build-source-package

build-source-package: clean rst-description-file
	./setup.py sdist

install-user: clean rst-description-file
	./setup.py install --user

install: clean rst-description-file
	./setup.py install

uninstall-user:
	$(PIP) uninstall $(PROJECT)

uninstall:
	$(PIP) uninstall $(PROJECT)

test:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); py.test $(PROJECT)

## Check correctness of the `.travis.yml` file
check-travis:
	travis-lint

check-package-metatada: rst-description-file
	./setup.py check --restructuredtext

html-readme:
	mkdir -p tmp
	pandoc -N -t html -s --no-wrap -o tmp/README.html README.md

run-oozie2oozie_yaml-example-complex:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat examples/example_workflow/workflow.xml | ./scripts/vipe-oozie2oozie_yaml

run-oozie2oozie_yaml-example-simple:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat vipe/oozie/test/data/javamapreduce/workflow.xml | ./scripts/vipe-oozie2oozie_yaml

run-oozie_yaml2pipeline-example-complex:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat examples/example_workflow/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline

run-oozie_yaml2pipeline-example-simple:
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat vipe/oozie/test/data/javamapreduce/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline

run-pipeline2dot-example-complex:
	mkdir -p tmp
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat examples/example_workflow/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline | ./scripts/vipe-pipeline2dot

run-pipeline2dot-example-simple:
	mkdir -p tmp
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat vipe/oozie/test/data/javamapreduce/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline | ./scripts/vipe-pipeline2dot

run-pipeline2png-example-complex:
	mkdir -p tmp
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat examples/example_workflow/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline | ./scripts/vipe-pipeline2dot | dot -Tpng > tmp/complex.png

run-pipeline2png-example-simple:
	mkdir -p tmp
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR); cat vipe/oozie/test/data/javamapreduce/workflow.xml | ./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline | ./scripts/vipe-pipeline2dot | dot -Tpng > tmp/simple.png

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
	$(PIP) install --user -i https://testpypi.python.org/pypi $(PROJECT)

upload-to-pypi: rst-description-file
	./setup.py sdist bdist_egg bdist_wheel upload -r pypi
