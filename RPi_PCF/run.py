from pcf8574 import PCF8574
from time import sleep

i2c_port_num = 1

pcf_read_address = 0x38
pcf_write_address = 0x3f

pcf_read = PCF8574(i2c_port_num, pcf_read_address)
pcf_write = PCF8574(i2c_port_num, pcf_write_address)

while 1:
	print('Read Port')
	print(pcf_read.port)
	print('Write Port')
	print(pcf_write.port)

	for i, pin_read,pin_write in zip(list(range(0,len(pcf_read.port))),pcf_read.port,pcf_write.port):
		if pin_read != pin_write:
			print('pin {} has read {} and write {}'.format(i,pin_read,pin_write))
			pcf_write.port[i] = pin_read
			print('pin updated')

	sleep(2)



