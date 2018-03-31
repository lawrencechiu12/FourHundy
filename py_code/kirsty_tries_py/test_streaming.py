import sqlite3
import plotly.ploty as py
import time
import sys
from plotly.graph_objs import Scatter, Layout, Figure
import serial

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2 = 'cv8vfh7m5j'
stream_token3 = 'fzr4foq2t6'

ser = serial.Serial('/dev/ttyACM0',9600)

conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()

def logData(hum, temp, press):
	curs.execute("INSERT INTO DHT_data VALUES(datetime('now'),datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?),(?),(?))",(hum,temp,press))
	conn.commit()
	time.sleep(5)

def pullData():
	read_line = ser.readline()
	line_str = read_line.decode("utf-8")
	if line_str == "Data:\n":
		humidity = float(ser.readline().decode("utf-8"))
		temperature = float(ser.readline().decode("utf-8"))
		pressure = float(ser.readline().decode("utf-8"))
		logData(humidity, temperature, pressure)
		status = 1
		print(humidity,temperature,pressure)
	else:
		#print("looking for data")
		#print(line_str)
		time.sleep(2)
		status = 0
	return status

py.sign_in(username, api_key)
stream1 = py.Stream(stream_token1)
stream1.open()
stream2 = py.Stream(stream_token2)
stream2.open()
stream3 = py.Stream(stream_token3)
stream3.open()

while True:
	found  = pullData()
	if  found == 1:
		t1, tp1, h1, p1 = getLastData()
		stream1.write(dict(x = t1, y = tp1))
		stream2.write(dict(x = t1, y = h1))
		stream3.write(dict(x = t1, y = p1))
