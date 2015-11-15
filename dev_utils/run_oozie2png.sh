#!/bin/bash

## Convert Oozie XML file to a diagram in PNG format.
## Generate a separate file for each possible detail level.

WORKFLOW_PATH=$1
OUTPUT_PATH_PREFIX=$2

MY_CURR_DIR=$(pwd)
MY_PYTHON_PATH=$PYTHONPATH

DETAIL_LEVEL_ARRAY=([0]=lowest low medium high very_high highest)
DETAIL_LEVEL_ARRAY_LENGTH=${#DETAIL_LEVEL_ARRAY[@]}

for (( i=0; i<$DETAIL_LEVEL_ARRAY_LENGTH; i++ ))
do
	DETAIL_LEVEL=${DETAIL_LEVEL_ARRAY[$i]}
	export PYTHONPATH=$MY_PYTHON_PATH:$MY_CURR_DIR; cat $WORKFLOW_PATH | ./scripts/vipe-oozie2png --detail_level $DETAIL_LEVEL --show_input_ports --show_output_ports > ${OUTPUT_PATH_PREFIX}-${i}_${DETAIL_LEVEL}_detail.png
done


