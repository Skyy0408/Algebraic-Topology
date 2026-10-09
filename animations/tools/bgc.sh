#!/bin/bash
# usage: tools/bgc.sh <cores> <q> <file.py> <Scene>...   serial render, cores e.g. 26,27
source /home/nthuuser/data/Sky/at/tools/activate.sh
cd /home/nthuuser/data/Sky/at/scenes
C=$1; Q=$2; F=$3; shift 3
for S in "$@"; do
  nice -n 19 taskset -c "$C" manim -$Q --media_dir ../media "$F" "$S" 2>&1 | grep -E "Error|Exception|Rendered"
done
echo DONE
