

name=${1:-STB-1/firmware}
rate=${2:-115200}
name=$(echo $name | rev | cut -f 2- -d '.' | rev)
echo "firmware name: $name.hex upload with baudrate $rate"
sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyUSB0 -b $rate -D -U flash:w:"$name.hex":i
