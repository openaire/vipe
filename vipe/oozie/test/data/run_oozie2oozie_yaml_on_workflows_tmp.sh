#!/bin/bash

PROJECT_ROOT_DIR=../../../..

ABSOLUTE_PROJECT_ROOT_DIR=$(cd $PROJECT_ROOT_DIR; pwd)
MY_PYTHON_PATH=$PYTHONPATH

for f in "subworkflow_with_root_ports/workflow.xml"
do
	echo "Running on '$f' ..."
	DIR=$(dirname "$f")
	export PYTHONPATH=$PYTHONPATH:$ABSOLUTE_PROJECT_ROOT_DIR; cat $f | $ABSOLUTE_PROJECT_ROOT_DIR/scripts/vipe-oozie2oozie_yaml > $DIR/workflow.yaml
	echo "Done."
done
