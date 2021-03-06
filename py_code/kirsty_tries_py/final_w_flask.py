import sys
import time
import sqlite3
import serial
import plotly.plotly as py
from plotly.graph_objs import Scatter, Figure, Layout, Stream
#for uart
from time import sleep
from math import log
from flask import flask
#plotly declarations
#arduino + database declarations
ser = serial.Serial('/dev/ttyACM0',9600)
conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()
#declation for uart communication
ser_uart = serial.Serial('/dev/ttyAMA0',9600)
ser_uart.timeout = 0
ser_uart.flushInput()
#functions for UART
def logData(status):
	curs.execute("INSERT INTO MOTION_stat VALUES(datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?))",(status,))
	conn.commit()
	time.sleep(1)

def pull_uart(prev_status):
	status = prev_status #if a valid message is recieved, this changes
	if ser_uart.inWaiting() > 0:
		char=ser_uart.read(1)
		if char == 'a':
			sleep(0.01)
			message = 'a'+ser_uart.read(11)
			print(message)
			if message == "a31BUTTONON-":
				status = 1
				if status != prev_status:
					logData(status)
					print(status)
					#message == "\0"
					import motion_alert
					#sudo python /home/pi/FourHundy/final/Scripts/motion_alert.py
			elif message == "a31BUTTONOFF":
				status = 0
				if status != prev_status:
					logData(status)
					print(status)
					#message == "\0"
	else:
		print("Waiting for Status")
		#message == "\0"
		#time.sleep(2)
		#sleep(1)
	return status

#for finding numSamples
def maxRowsTable():
	for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
		maxNumberRows = row[0]
	return maxNumberRows

def check_numSamples(numSamples):
	if numSamples < 100:
		numSamples = maxRowsTable()
	else:
		numSamples = 100
	return numSamples

#getting data from database
def getHistData (numSamples):
	curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	datesLOC = []
	temps = []
	hums = []
	press = []
	for row in reversed(data):
		datesLOC.append(row[1])
		hums.append(row[2])
		temps.append(row[3])
		press.append(row[4])
	return datesLOC, temps, hums, press

def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT 1"):
		dateLOC = str(row[1])
		temp = row[3]
		hum = row[2]
		press = row[4]
	return dateLOC, temp, hum, press
    
#getting data from Arduino
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
		#time.sleep(1)
		status = 0
	return status

#logs data from arduino
def logData(hum, temp, press):
	curs.execute("INSERT INTO DHT_data VALUES(datetime('now'),datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?),(?),(?))",(hum,temp,press))
	conn.commit()

#functions plotting

#variables
global numSamples
numSamples = 0
prev_status = 0

#flask operation
@app.route("/")
def index():
    time, temp, hum, press = getLastData()
    templateData = {
        'time' : time,
        'temp' : temp,
        'hum' : hum,
        'press' : press
    }
    return render_template('index.html', **templateData_)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80, debug=True)
