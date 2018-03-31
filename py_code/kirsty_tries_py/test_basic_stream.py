import sys
import plotly.plotly as py
from plotly.graph_objs import *

username = 'kirstycha'
api_key = 'IGTdhsbggLKYae1wi7Ej'
stream_token1 = 'a9kvj05v66'
stream_token2 = 'cv8vfh7m5j'
stream_token3 = 'fzr4foq2t6'

py.sign_in(username,api_key)

trace0 = Scatter(
	x=[],
	y=[],
	mode = 'lines+markers',
	name = 'test',
	stream = dict(
		token=stream_token1,
		maxpoints = 100
	)
)
layout = Layout(title= 'layout')
fig = Figure(data=[trace0], layout = layout)
print py.plot(fig, filename = 'test')

ha = 1
ba = 5

while True:
	stream1 = py.Stream(stream_token1)
	stream1.open()
	stream1.write({'x': ha, 'y': ba})
	print("i wrote")
	stream1.close()
	ha = ba*4
	ba = ha-6
