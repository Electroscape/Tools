# How To Setup

## Pre-installation

1. Connect the nfc sensor to the i2c pin on the rpi
2. From `sudo raspi-config` enable i2c

## Installation

1. run `bash install.sh`
2. Edit and add to the end of the file  `sudo nano /etc/nfc/libnfc.conf`

    ```bash
    device.name = "PN532 over I2C"
    device.connstring = "pn532_i2c:/dev/i2c-1"
    ```

3. run `i2cdetect -y 1` to assure i2c sensor is detected corretly. Default address is 0x24

**Hint**

To install the packages system-wide, use:

`python3 -m pip config set global.break-system-packages true`

Otherwise, create venv and install the packages in it. After that install the req.txt

`pip3 install -r requirements.txt`

## Run App

Start the script with python3 in the console of the rpi

`bash run.sh` or double click the desktop launcher `nfc_reader.desktop`

it will ask you what room shall be used, those are configured in cfg.json

then you can either read or write.

If, items are missing feel free to add them to the json 

## Troubleshooting 

### ModuleNotFoundError: No module named 'board'

`sudo python3 -m pip install --break-system-packages --force-reinstall adafruit-blinka`

### locale.Error: unsupported locale setting

- Check location setting with `locale`
- Install german location `sudo locale-gen de_DE.UTF-8`
- Run `sudo dpkg-reconfigure locales` and choose de_DE from the list using space
- in `run.sh` add before python call:
  ```Bash
    # Set locale for German (Germany)
    export LC_ALL=de_DE.UTF-8
    export LANG=de_DE.UTF-8
    export LANGUAGE=de_DE.UTF-8
    ```

### For RPi 5: gpio missing

in requirements, install `rpi-lgpio` instead of `RPi.GPIO`
