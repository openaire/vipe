#!/bin/bash

## Convert Oozie XML file to a Pipeline representation in YAML format.

WORKFLOW_PATH=$1

MY_CURR_DIR=$(pwd)
MY_PYTHON_PATH=$PYTHONPATH

export PYTHONPATH=$MY_PYTHON_PATH:$MY_CURR_DIR; cat $WORKFLOW_PATH | \
	./scripts/vipe-oozie2oozie_yaml

