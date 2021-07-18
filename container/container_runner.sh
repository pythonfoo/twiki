#!/bin/bash

if [ -z "$INTERVAL" ]
then
    echo "INTERVAL environment is empty, using default of 300 seconds / 5 min"
    export INTERVAL=300
fi


while :
do
    python tweet.py
    sleep  "$INTERVAL"
done

