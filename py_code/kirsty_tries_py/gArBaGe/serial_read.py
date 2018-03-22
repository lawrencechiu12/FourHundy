import serial

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]
while True:
	read_serial=ser.readline()
#	s[0] = ser.readline()
#	print s[0]
	#if(type(read_serial)!='string'):
	#	print (float(read_serial))
	print(type(read_serial))
	print(read_serial)
