#!/bin/bash
INPUT_JSON="../ex00/hh.json"  
OUTPUT_CSV="hh.csv"
jq -r -f filter.jq "$INPUT_JSON" > "$OUTPUT_CSV"
