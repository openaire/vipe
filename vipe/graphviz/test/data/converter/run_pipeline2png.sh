#!/bin/bash

PROJECT_ROOT_DIR=../../../../..

ABSOLUTE_PROJECT_ROOT_DIR=$(cd $PROJECT_ROOT_DIR; pwd)

mkdir -p tmp

for f in $(find . -name "*.yaml")
do
	echo "Running on '$f' ..."
	DIR=$(dirname "$f")
	export PYTHONPATH=$PYTHONPATH:$ABSOLUTE_PROJECT_ROOT_DIR; cat $f | $ABSOLUTE_PROJECT_ROOT_DIR/scripts/vipe-pipeline2dot --show_input_ports --show_output_ports --detail_level highest | $ABSOLUTE_PROJECT_ROOT_DIR/scripts/vipe-dot2png > $DIR/tmp/$f.png
	echo "Done."
done
