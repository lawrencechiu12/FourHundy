import sqlite3
import time
import sys



def getData(num):
	conn = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(num))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
#	pres = []
	conn.close()
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
#		pres.append(row[3])
#	return dates, temps, hums, pres #add in pres later
	return dates, temps, hums

def writeData(num):
	file = open("/home/pi/FourHundy/webserver2.0/sensor_database/DataFile.txt","w+")

	file.write(" Date				Temperature	 Humidity	Pressure\n")
	for x in range(0,num):
		file.write(" " + (str(dates[x])) + "		" + (str(temps[x])) + "		 " + (str(hums[x])) + "\n") # add in pressure later

	file.close()


#times, temps, hums, pres = getData(6)
dates, temps, hums = getData(6)
writeData(6)

