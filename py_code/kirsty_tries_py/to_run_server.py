import serial
import sqlite3
import sys
import time
import plotly.ploty as py
from plotly.graph_objs import Scatter, Layout, Figure
#from flask import Flask, render_template
#stuff for plotly
username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2 = 'cv8vfh7m5j'
stream_token3 = 'fzr4foq2t6'
#for flask operation
#app = Flask(__name__)
#serial port  and baud rate
ser = serial.Serial('/dev/ttyACM0',9600)
#to connect to database
conn = sqlite3.connect('sensorsData.db') #if py code lives w sensorsDataTest.db
curs = conn.cursor()

def plot_1(x_data,y_data,data_name):
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
    plot_1(x_data, temp, "Temperature")
    plot_1(x_data, hum, "Humidity")
    plot_1(x_data, press, "Pressure")

def sign_in_plotly():
    py.sign_in(username, api_key)
    stream1 = py.Stream(stream_token1)
    stream1.open()
    stream2 = py.Stream(stream_token2)
    stream2.open()
    stream3 = py.Stream(stream_token3)
    stream3.open()

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
		#print(humidity,temperature,pressure)
	else:
		#print("looking for data")
		#print(line_str)
		time.sleep(2)
def getLastData():
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT 1"):
        dateLOC = str(row[1])
        temp = row[2]
        hum = row[3]
        press = row[4]
    return dateLOC, temp, hum, presss

def getHistData (numSamples):
#    conn = sqlite3.connect('sensorsData.db')
#    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    datesLOC = []
    temps = []
    hums = []
    press = []
#    conn.close()
    for row in reversed(data):
        datesLOC.append(row[1])
        temps.append(row[2])
        hums.append(row[3])
        press.append(row[4])
    return datesLOC, temps, hums, press

def maxRowsTable():
    for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
        maxNumberRows = row[0]
    return maxNumberRows

def check_numSamples():
    if numSamples < 100:
        numSamples = maxRowsTable()


#define and initialize global variables
global numSamples
global stream1, stream2, stream3
pullData()
numSamples = 0
check_numSamples()
times, temps, hums, press = getHistData(numSamples)
sign_in_plotly()
plot_3(times, temps, hums, press)

while True:
    pullData()
    t1, tp1, h1, p1 = getLastData()
    stream1.write({'x': t1, 'y': tp1})
    stream2.write({'x': t1, 'y': h1})
    stream3.write({'x': t1, 'y': p1})




#@app.route("/")
#def index():
#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80, debug=False)
