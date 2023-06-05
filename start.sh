#!/bin/bash

# https://stackoverflow.com/questions/51903588/python-script-not-starting-with-etc-rc-local


echo "Starting alarm app ." > /tmp/startup_thing.log

cd "$(dirname "$0")"

python3 AlarmMain.py

