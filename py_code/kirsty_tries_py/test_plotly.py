#code to test plotly
import sqlite3
import plotly,plotly as py
import time
from plotly.graph_objs import Scatter, Layout, Figure

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token = 'a9kvj05v66'

def plot_it(x_data, y_data):
    trace1 = Scatter(
        x=x_data,
        y=y_data,
        stream = dict(
            token=stream_token,
            maxpoints = 100
            )
        )
    layout = Layout(title="my plot")
    fig = Figure(data=[trace1], layout = layout)
    print py.plot(fig, filename = 'my plot')

def getHistData (numSamples):
    curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
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

py.sign_in(username, api_key)
times, temps, hums, press = getHistData(10)
plot_it(times, temps)
stream = py.Stream(stream_token)
stream.open()
