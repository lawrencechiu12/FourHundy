
import serial
import sqlite3
import sys
import time
from time import sleep
from math import log


ser = serial.Serial('/dev/ttyAMA0',9600)
ser.timeout = 0
ser.flushInput()

def logData(status):
	conn = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	#curs.execute("INSERT INTO MOTION_stat VALUES(datetime(strftime('now'),(?))",(status))
	curs.execute("INSERT INTO MOTION_stat VALUES(datetime(strftime('%Y-%m-%d %H:%M:%S','now','localtime')),(?))",(status,))
	conn.commit()
	conn.close()
	time.sleep(5)

while True:
	if ser.inWaiting() > 0:
		char=ser.read(1)
		if char == 'a':
			sleep(0.01)
			message = 'a'+ser.read(11)
			print(message)

		if message == "a31BUTTONON-":
			status = 1
			logData(status)
			print(status)
			message == "\0"

		elif message == "a31BUTTONOFF":
			status = 0
			logData(status)
			print(status)
			message == "\0"

		else:
			print("Waiting for Status")
			message == "\0"
			time.sleep(2)
