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

def plot_it(x_data, temp, hum, press):
    trace0 = Scatter(
        x=x_data,
        y=temp,
        mode = 'lines+markers'
        name = 'Temperature(Celsius)'
        stream = dict(
            token=stream_token,
            maxpoints = 100
            )
        )
    trace1 = Scatter(
        x=x_data,
        y=hum,
        mode = 'lines+markers'
        name = 'Humidity(%)'
        stream = dict(
            token=stream_token,
            maxpoints = 100
            )
        )
    trace2= Scatter(
        x=x_data,
        y=press,
        mode = 'lines+markers'
        name = 'Pressure(kpa)'
        stream = dict(
            token=stream_token,
            maxpoints = 100
            )
        )
    layout = Layout(title="Home Conditions")
    fig = Figure(data=[trace0, trace1, trace2], layout = layout)
    print py.plot(fig, filename = 'home conditions')

def getHistData (numSamples):
    conn = sqlite3.connect('sensorsData.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    #datesUTC = []
    datesLOC = []
    temps = []
    hums = []
    press = []
    conn.close()
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
