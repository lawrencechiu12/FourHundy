#testing plotly with multiple lines of data to plot
#code to test plotly
import sqlite3
import plotly.plotly as py
import time
import sys
from plotly.graph_objs import Scatter, Layout, Figure

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token = 'a9kvj05v66'

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

def getHistData (numSamples):
#    conn = sqlite3.connect('sensorsData.db')
#    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    #datesUTC = []
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

global numSamples
numSamples = maxRowsTable()
if( numSamples > 101):
    numSamples = 100

py.sign_in(username, api_key)
times, temps, hums, press = getHistData(numSamples)
plot_it(times, temps, hums, press)
stream = py.Stream(stream_token)
stream.open()
