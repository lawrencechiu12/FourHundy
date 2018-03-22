import serial
from flask import Flask, render_template
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0',9600)

@app.route("/")
def index():
