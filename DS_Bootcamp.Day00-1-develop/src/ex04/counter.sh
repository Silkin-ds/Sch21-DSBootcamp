#!/bin/bash

FROM="../ex03/hh_positions.csv"

echo "\"name\",\"count\"" > hh_uniq_positions.csv

tail -n +2 "$FROM" | cut -d ',' -f 3 | sort | uniq -c | sort -nr | awk '{
    print $2 "," $1 
}'>> hh_uniq_positions.csv