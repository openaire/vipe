#!/bin/bash

PROJECT_ROOT_DIR=../../../..

ABSOLUTE_PROJECT_ROOT_DIR=$(cd $PROJECT_ROOT_DIR; pwd)
MY_PYTHON_PATH=$PYTHONPATH

for f in $(find . -name "workflow.xml")
do
	echo "Running on '$f' ..."
	DIR=$(dirname "$f")
	export PYTHONPATH=$PYTHONPATH:$ABSOLUTE_PROJECT_ROOT_DIR; $ABSOLUTE_PROJECT_ROOT_DIR/scripts/vipe-oozie2yaml < $f > $DIR/workflow.yaml
	echo "Done."
done
