import sqlite3
import time
import sys
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import serial

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2 = 'cv8vfh7m5j'
stream_token3 = 'fzr4foq2t6'

ser = serial.Serial('/dev/ttyACM0',9600)
conn = sqlite3.connect('sensorsData.db')
curs = conn.cursor()

def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT 1"):
		dateLOC = str(row[1])
		temp = row[2]
		hum = row[3]
		press = row[4]
	return dateLOC, temp, hum, press
def getHistData(numSamples):
	curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	datesLOC = []
	temps = []
	hums = []
	press = []
	for row in reversed(data):
		datesLOC.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
		press.append(row[4])
	return datesLOC, temps, hums, press

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
	else:
		time.sleep(2)
		status = 0
	return status

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

def maxRowsTable():
	for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
		maxNumberRows = row[0]
	return maxNumberRows

def check_numSamples(numSamples):
	if numSamples < 100:
		numSamples = maxRowsTable()
	return numSamples

global numSamples
global stream1, stream2, stream3
found = pullData()
numSamples = 0
numSamples = check_numSamples(numSamples)
times, temps, hums, press = getHistData(numSamples)
py.sign_in(username, api_key)
stream1 = py.Stream(stream_token1)
stream1.open()
stream2 = py.Stream(stream_token2)
stream2.open()
stream3 = py.Stream(stream_token3)
stream3.open()
plot_3(times, temps, hums, press)

while True:
	found  = pullData()
	if  found == 1:
		t1, tp1, h1, p1 = getLastData()
		stream1.write({'x': t1, 'y': tp1})
		stream2.write({'x': t1, 'y': h1})
		stream3.write({'x': t1, 'y': p1})
