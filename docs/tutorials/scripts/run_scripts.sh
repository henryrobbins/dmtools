#!/bin/bash
declare -a dirs=("python" "numpy" "dmtools")

for dir in "${dirs[@]}"
do
    cd $dir
    for f in *.py; do python "$f"; done
    cd ..
done
