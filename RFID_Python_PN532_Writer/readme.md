# How To Setup

## Installation

To install the packages system-wide, use:

`python3 -m pip config set global.break-system-packages true`

Otherwise, create venv and install the packages in it. After that install the req.txt

`pip3 install -r requirements.txt`

## Run App

Start the script with python3 in the console of the raspberry

`python3 rfid_rw.py`

it will ask you what room shall be used, those are configured in cfg.json

then you can either read write or duplicate.

If, items are missing feel free to add them to the json 

## Troubleshooting 

ModuleNotFoundError: No module named 'board'
sudo python3 -m pip install --break-system-packages --force-reinstall adafruit-blinka 
