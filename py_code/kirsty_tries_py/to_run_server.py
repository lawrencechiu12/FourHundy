import serial
import sqlite3
import sys
import time
import plotly.ploty as py
from flask import Flask, render_template
app = Flask(__name__)
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
		#print(humidity,temperature,pressure)
	else:
		#print("looking for data")
		#print(line_str)
		time.sleep(2)

def getHistData (numSamples):
    curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    dates = []
    temps = []
    hums = []
    press = []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
        press.append(row[3])
    return dates, temps, hums, press

def maxRowsTable():
    for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
        maxNumberRows = row[0]
    return maxNumberRows

#define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if( numSamples > 101):
    numSamples = 100

@app.route("/")
def index():


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
