#!/bin/bash
sudo pkill python

# cd to this script dir
# fixes activate venv from crontab 
cd "${0%/*}"

# shellcheck disable=SC2164
source venv/bin/activate
sleep 1

export DISPLAY=:"0.0" 
python main.py &