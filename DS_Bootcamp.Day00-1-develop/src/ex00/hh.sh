#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "error: not correct parameter"
    exit 1
fi
name=$1
curl -s "https://api.hh.ru/vacancies?text=${name}&search_field=name&per_page=20" | jq '.' > hh.json

if [ $? -ne 0 ]; then 
    echo "error"
    exit 1
fi