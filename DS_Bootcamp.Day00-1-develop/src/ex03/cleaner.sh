#!/bin/bash

OUT="hh_positions.csv"
FROM="../ex02/hh_sorted.csv"

head -n 1 "$FROM" > "$OUT"

tail -n +2 "$FROM"  | awk -F '",' 'BEGIN { OFS="," } {
    position = ""
    if ($3 ~ /Junior/) position = "Junior"
    if ($3 ~ /Middle/) position = (position == "" ? "Middle" : position "/Middle")
    if ($3 ~ /Senior/) position = (position == "" ? "Senior" : position "/Senior")
    if (position == "") position = "-"
    $3 = "\"" position "\""
    print $0
}' >> hh_positions.csv