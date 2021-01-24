Physical and RPI setup as follows

Enable I2C interface on the Pi raspi config
sudo apt install i2c-tools

/etc/nfc/libnfc.conf

device.name = "PN532 over I2C"
device.connstring = "pn532_i2c:/dev/i2c-1"

wiring:
# NFC module pin -> Pi GPIO physical pin #
GND -> 6
VCC -> 4
SDA -> 3
SCL -> 5

i2cdetect -y 1
# should be on 24

nfc-poll


or the original source:
https://blog.stigok.com/2017/10/12/setting-up-a-pn532-nfc-module-on-a-raspberry-pi-using-i2c.html


adafruit_pn532 seems to work
https://github.com/adafruit/Adafruit_CircuitPython_PN532/tree/master/examples

sweet revenge is on Auth A check 
smb://teamescape-nas.local/team-tfm/Z_Material%20Robert/Software/Süße_Rache/SuesseRache-HH-Fingerabdruckscanner/MFRC522-python/Write.py
