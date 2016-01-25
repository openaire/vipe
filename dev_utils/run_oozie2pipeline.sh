#!/bin/bash

## Convert Oozie XML file to its YAML representation.

WORKFLOW_PATH=$1

MY_CURR_DIR=$(pwd)
MY_PYTHON_PATH=$PYTHONPATH

export PYTHONPATH=$MY_PYTHON_PATH:$MY_CURR_DIR; cat $WORKFLOW_PATH | \
	./scripts/vipe-oozie2oozie_yaml | ./scripts/vipe-oozie_yaml2pipeline


