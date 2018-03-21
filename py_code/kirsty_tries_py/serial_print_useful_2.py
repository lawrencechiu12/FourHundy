import serial
import sqlite3
import sys
import time

ser = serial.Serial('/dev/ttyACM0',9600)

def logData(hum, temp, press):
	con = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	curs.execute("INSERT INTO DHT_data(datetime('now'),(?),(?),(?)",(humidity,temperature,pressure))
	conn.commit()
	time.sleep(5)

while True:
	read_line = ser.readline()
	if readline == "data":
		humidity = float(ser.readline)
		temperature = float(ser.readline)
		pressure = float(ser.readline)
		logData(humidity, temperature, pressure)
	else:
		print("looking for data")
		print(readline)
		time.sleep(2)
