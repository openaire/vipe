#!/bin/bash

source ../generate_images.sh

ROOT_DIR=$(pwd)/../../..

generate $ROOT_DIR $ROOT_DIR/examples/iis_workflows/primary-main.xml \
	medium primary-main-medium_detail.png \
	--show_input_ports --show_output_ports
generate $ROOT_DIR $ROOT_DIR/examples/iis_workflows/primary-processing.xml \
	low primary-processing-lowest_detail.png \
	--show_input_ports --show_output_ports
generate $ROOT_DIR $ROOT_DIR/examples/iis_workflows/primary-processing.xml \
	medium primary-processing-medium_detail.png \
	--show_input_ports --show_output_ports
	
