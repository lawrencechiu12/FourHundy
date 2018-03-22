import serial

ser = serial.Serial('/dev/ttyACM0',9600)
#s = [0,1]
while True:
	read_serial=ser.readline()
	if read_serial == "Data:\n":
		print("I read the data line")
		for i in range (0,2):
			value = float(ser.readline())
			print(value)
	else:
#	s[0] = ser.readline()
#	print s[0]
		print("Data not found")
