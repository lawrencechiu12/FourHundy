import sys
import time
import sqlite3
import serial
import plotly.plotly as py
from plotly.graph_objs import Scatter, Figure, Layout, Stream

#declarations for writing to plotly
username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2='cv8vfh7m5j'
stream_token3='fzr4foq2t6'

#declaration for serial communication
ser = serial.Serial('/dev/ttyACM0',9600)
conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()

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
		temps.append(row[2])
		hums.append(row[3])
		press.append(row[4])
	return datesLOC, temps, hums, press

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
		#print(humidity,temperature,pressure)
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

#plotting in plotly 
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
global numSamples
numSamples = 0

while True:
    #read from arduino
	found = pullData()
	if found == 1:
        #plot in plotly if something found 
		numSamples = check_numSamples(numSamples)
		time, temp, hum, press = getHistData(numSamples)
		plot_3(time, temp, hum, press)
        #check for large change 
        sudo python /home/pi/FourHundy/final/scripts/comparedict.py

