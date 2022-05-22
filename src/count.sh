#!/bin/bash
# Fun little script to print number of lines in a project. Will only look for 
# .py scripts

total_lines=0

for FILE in $(find ./ -name '*.py')
do 
    lines=$(cat $FILE | wc -l)
    total_lines=$(($lines + $total_lines))

done

echo Total lines: $total_lines
