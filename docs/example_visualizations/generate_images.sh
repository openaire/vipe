#!/bin/bash

ROOT_DIR=$(pwd)/../../..

function generate {
	ROOT_DIR=$1
	WORKFLOW_PATH=$2
	DETAIL_LEVEL=$3
	OUTPUT=$4
	OPTION_1=${5-""}
	OPTION_2=${6-""}
	export PYTHONPATH=$PYTHONPATH:$ROOT_DIR; cat $WORKFLOW_PATH | \
		$ROOT_DIR/scripts/vipe-oozie2png --detail_level $DETAIL_LEVEL \
		--horizontal_orientation $OPTION_1 $OPTION_2 --show_output_ports > \
		$OUTPUT
}
