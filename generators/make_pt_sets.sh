#!/bin/bash

DIR=/home/cfillmor/topology/bing/bing_anim/longer/

for value in $(ls $DIR)
do
	while [ $(jobs | wc -l) -ge 7 ] ; do sleep 1 ; done
	python make_medial_pt_sets.py $value &
done

echo All done
