import sys
import time
import sqlite3
import serial
import plotly.plotly as py
from plotly.graph_objs import Scatter, Figure, Layout, Stream

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2='cv8vfh7m5j'
stream_token3='fzr4foq2t6'

ser = serial.Serial('/dev/ttyACM0',9600)

conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()

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

def getHistData (numSamples):
#    conn = sqlite3.connect('sensorsData.db')
#    curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	datesLOC = []
	hums = []
	temps = []
	press = []
#    conn.close()
	for row in reversed(data):
		datesLOC.append(row[1])
		hums.append(row[2])
		temps.append(row[3])
		press.append(row[4])
	return datesLOC, temps, hums, press

def pullData():
	read_line = ser.readline()
	line_str = read_line.decode("utf-8")
	if line_str == "Data:\n":
		humidity = float(ser.readline().decode("utf-8"))
		temperature = float(ser.readline().decode("utf-8"))
		pressure = float(ser.readline().decode("utf-8"))
		logData(humidity, temperature, pressure)
		status = 1
		#print(humidity,temperature,pressure)
	else:
		#print("looking for data")
		#print(line_str)
		#time.sleep(1)
		status = 0
	return status

def logData(hum, temp, press):
	curs.execute("INSERT INTO DHT_data VALUES(datetime('now'),datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?),(?),(?))",(hum,temp,press))
	conn.commit()
	#time.sleep(1)

def plot_1(x_data,y_data,data_name, stream_token):
	trace0 = Scatter(
		x=x_data,
		y=y_data,
		mode = 'lines+markers',
		name = data_name,
		stream = dict(
			token=stream_token,
			maxpoints = 100
		)
	)
	layout = Layout(title= data_name)
	fig = Figure(data=[trace0], layout = layout)
	print py.plot(fig, filename = data_name)

def plot_3(x_data, temp, hum, press):
	plot_1(x_data, temp, "Temperature", stream_token1)
	plot_1(x_data, hum, "Humidity", stream_token2)
	plot_1(x_data, press, "Pressure", stream_token3)

py.sign_in(username,api_key)

#stream1 = py.Stream(stream_token1)
#stream1.open()
#stream2 = py.Stream(stream_token2)
#stream2.open()
#stream3 = py.Stream(stream_token3)
#stream3.open()

global numSamples
numSamples = 0

while True:
	found = pullData()
	if found == 1:
		numSamples = check_numSamples(numSamples)
		time, temp, hum, press = getHistData(numSamples)
		plot_3(time, temp, hum, press)
