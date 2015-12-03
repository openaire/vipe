#!/bin/bash

PROJECT_ROOT_DIR=../../../..

ABSOLUTE_PROJECT_ROOT_DIR=$(cd $PROJECT_ROOT_DIR; pwd)

for f in "subworkflow_with_root_ports/workflow.yaml"
do
	echo "Running on '$f' ..."
	DIR=$(dirname "$f")
	export PYTHONPATH=$PYTHONPATH:$ABSOLUTE_PROJECT_ROOT_DIR; cat $f | $ABSOLUTE_PROJECT_ROOT_DIR/scripts/vipe-oozie_yaml2pipeline > $DIR/pipeline.yaml
	echo "Done."
done
