import sqlite3
import time
import sys
import plotly.plotly as py
from plotly.graphs_objs import Scatter, Data, Layout, Figure, Stream

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2 = 'cv8vfh7m5j'
stream_token3 = 'fzr4foq2t6'

py.sign_in(username, api_key)
stream1 = py.Stream(stream_token1)
stream1.open()
stream1.write({'x': 1, 'y': 1})

while True:
    ha = 1
    ba = 4
    stream1.write({'x': ha, 'y': ba})
    ha = ba*4
    ba = ha-6
