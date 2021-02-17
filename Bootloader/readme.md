# on the Raspberry Pi: Download optiboot bootloader file and enter root mode 
wget https://raw.githubusercontent.com/Optiboot/optiboot/master/optiboot/bootloaders/optiboot/optiboot_atmega328.hex
sudo bash 

# unlock the boot sector 
/opt/avrdude/bin/avrdude -p atmega328p -c linuxgpio -U lock:w:0x3f:m 

# write boot loader and lock the boot sector against accidental writes (in the lock byte) 
/opt/avrdude/bin/avrdude -p atmega328p -c linuxgpio -u -U flash: w: optiboot_atmega328.hex -U lock:w:0x0F:m 

# reading the lock byte: 
/opt/avrdude/bin/avrdude -p atmega328p -c linuxgpio -vv -U lock:r:lock_byte.bin:r 
hexdump -C lock_byte.bin

source: https://www.torsten-traenkner.de/linux/raspberry/arduino.php
Please be aware of the raspi pins used and the configuration file
