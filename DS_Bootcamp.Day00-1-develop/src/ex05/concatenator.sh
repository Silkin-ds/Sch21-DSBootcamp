#!/bin/bash

head -n 1 ../ex03/hh_positions.csv > hh_positions.csv
for file in *.csv; do
    if [ "$file" != "hh_positions.csv" ]; then
        tail -n +2 "$file" >> hh_positions.csv
    fi
done