#!/bin/bash

INPUT_FILE="./../ex03/hh_positions.csv"

tail -n +2 "$INPUT_FILE" | cut -d ',' -f 2 | cut -d 'T' -f 1 | sort | uniq | while read -r date; do
     clean_date=$(echo "$date" | tr -d '"')
    {
        head -n 1 "$INPUT_FILE"
        grep "$date" "$INPUT_FILE"
    } >> $clean_date.csv 
done