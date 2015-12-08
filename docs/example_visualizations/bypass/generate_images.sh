#!/bin/bash

source ../generate_images.sh

ROOT_DIR=$(pwd)/../../..
WORKFLOW_PATH=$ROOT_DIR/vipe/oozie/test/data/bypass/workflow.xml

generate $ROOT_DIR $WORKFLOW_PATH lowest detail_lowest-ports_none.png
generate $ROOT_DIR $WORKFLOW_PATH medium detail_medium-ports_none.png
generate $ROOT_DIR $WORKFLOW_PATH medium detail_medium-ports_input_output.png \
	--show_input_ports --show_output_ports
generate $ROOT_DIR $WORKFLOW_PATH highest detail_highest-ports_input_output.png \
	--show_input_ports --show_output_ports
	
