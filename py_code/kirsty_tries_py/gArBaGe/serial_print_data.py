import serial

ser = serial.Serial('/dev/ttyACM0',9600)
#s = [0,1]
while True:
	read_serial=ser.readline()
	read_in_string=read_serial.decode("utf-8")
	if read_in_string == "Data:\n":
		print("I read the data line")
		for i in range (0,3):
			print(i)
			#value_str = ser.readline()
			value = float(ser.readline().decode("utf-8"))
			print(value)
	else:
#	s[0] = ser.readline()
#	print s[0]
		print("Data not found")
		print(read_in_string)
