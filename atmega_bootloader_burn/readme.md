### install avrdude
`sudo apt-get install avrdude`

### modify linxGPIO configuration in avrdude.conf

 * `cd /etc`
 * `sudo nano avrdude.con`
 * jump to linuxgpio
 * uncomment and change to the following

```
programmer
  id    = "linuxgpio";
  desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
  type  = "linuxgpio";
  reset = 25;
  sck   = 11;
  mosi  = 10;
  miso  = 9;
;
```

### connect the arduino 

Arduino -> RPI  
Vin -> 3.3V  
GND -> GND  
RST -> 25  
11 -> 10 (SPIMOSI)  
12 -> 9 (SPIMISO)  
13 -> 11 (SPICLK)

### burn the bootloader

if during the follwing an issue arises with pin (25 here) being used
`echo 25 > /sys/class/gpio/unexport`

 * `sudo ./a_unlockBoot` 
 * `sudo ./b_writeBoot`