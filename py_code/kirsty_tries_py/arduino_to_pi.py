import serial
import sqlite3
import sys
import time

ser = serial.Serial('/dev/ttyACM0',9600)

def logData(hum, temp, press):
	conn = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	curs.execute("INSERT INTO DHT_data VALUES(datetime('now'),datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?),(?),(?))",(hum,temp,press))
	conn.commit()
	conn.close()
	time.sleep(5)

while True:
	read_line = ser.readline()
	line_str = read_line.decode("utf-8")
	if line_str == "Data:\n":
		humidity = float(ser.readline().decode("utf-8"))
		temperature = float(ser.readline().decode("utf-8"))
		pressure = float(ser.readline().decode("utf-8"))
		logData(humidity, temperature, pressure)
		print(humidity,temperature,pressure)
	else:
		print("looking for data")
		print(line_str)
		time.sleep(2)
