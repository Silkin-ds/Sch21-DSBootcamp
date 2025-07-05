#!/bin/bash

INPUT_CSV="../ex01/hh.csv"
OUTPUT_CSV="hh_sorted.csv"
HEADER=$(head -n 1 "$INPUT_CSV")
DATA=$(tail -n +2 "$INPUT_CSV" | sort -t ',' -k2,2 -k1,1)
echo "$HEADER" > "$OUTPUT_CSV"
echo "$DATA" >> "$OUTPUT_CSV"