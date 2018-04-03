import sys
import time
import sqlite3
import plotly.plotly as py
from plotly.graph_objs import Scatter, Figure, Layout, Stream

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2='cv8vfh7m5j'
stream_token3='fzr4foq2t6'

conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()

def maxRowsTable():
	for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
		maxNumberRows = row[0]
	return maxNumberRows

def check_numSamples():
	numSamples = maxRowsTable()
	if numSamples > 100:
		numSamples = 100
	return numSamples

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

numSamples = check_numSamples()
times, temp, hum, press = getHistData(numSamples)
plot3(times, temp, hum, press)
