import serial
import sqlite3 as lite
import sys
con = lite.connect('sensorsDATA.db')
ser = serial.Serial('/dev/ttyACM0',9600)
def read_serial():
	read_line = ser.readline()
	if readline != "/n":
		if readline == "Humidity:":
			humidity = int(ser.readline)

		elif readline == "Temperature:":
			temperature = int(ser.readline)
		elif readline == "Pressure:":
			pressure = int(ser.readline)
		else:
			print("No matching cases, I found:")
			print(readline);
			return
	else
		print(readline)
		return
while True:
	read_serial()
	print humidity
