#!/usr/bin/env bash

mkdir -p output
for i in *.png ; do
    temp_file="output/$i.temp.bmp"
    convert $i -depth 8 -background white -transparent-color '#123456' -flatten "$temp_file"
    convert $temp_file output/$i
    rm $temp_file
done
