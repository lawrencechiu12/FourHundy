import sqlite3
import time
import sys

num = 2
def getData(num):
	conn = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(num))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	#pres = []
	conn.close()
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		#pres.append(row[3])
	#return dates, temps, hums, pres
	return dates, temps, hums

#def compareData(dates, temps, hums, pres)
def compareData(dates, temps, hums)
	if abs(temps[0] - temps[1]) > 4:
		#do command
