#!/bin/bash
sudo pkill python

# cd to this script dir
# fixes activate venv from crontab 
cd "${0%/*}"

# shellcheck disable=SC2164
source venv/bin/activate
sleep 1

# Set locale for German (Germany)
# by default, the locale is set to en_GB.UTF-8
export LC_ALL=de_DE.UTF-8
export LANG=de_DE.UTF-8
export LANGUAGE=de_DE.UTF-8

export DISPLAY=:"0.0" 
python main.py &