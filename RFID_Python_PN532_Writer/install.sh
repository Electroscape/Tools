#!/bin/bash

sudo apt update -y
sudo apt install i2c-tools libnfc6 libnfc-bin libnfc-examples -y
sudo apt install python3-dev python3-rpi.gpio -y

sudo locale-gen de_DE.UTF-8

## uncomment if you want to set the locale
# sudo dpkg-reconfigure locales

# shellcheck disable=SC2164
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt