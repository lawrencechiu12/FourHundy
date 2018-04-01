import sqlite3
import time
import sys

conn = sqlite3.connect('sensorsData.db')
curs = conn.cursor()

# This function pulls the latest 6 sets of data from the database
def check_num():
	num = maxRowsTable()
	if num > 6:
		num = 6
	return num

def maxRowsTable():
	for row in curs.execute("SELECT COUNT(temp) from DHT_data"):
		maxNumberRows = row[0]
	return maxNumberRows

def getData(num):
	#conn = sqlite3.connect('sensorsData.db')
	#curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(num))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	pres = []
	conn.close()
	for row in reversed(data):
		dates.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
		pres.append(row[4])
	return dates, temps, hums, pres #add in pres later
#	return dates, temps, hums

#This function  writes the pulled data into a file in a readable format
def writeData(num, dates, temps, hums, pres):
	file = open("/home/pi/FourHundy/final/DataFile.txt","w+")
	file.write(" Date				Temperature		Humidity	Pressure\n")
	for x in range(0,num):
		file.write(" " + (str(dates[x])) + "			" + (str(temps[x])) + "		 " + (str(hums[x])) + "		"+(str(pres[x]))+"\n") # add in pressure later
	file.close()

numSamples = check_num()
dates, temps, hums, pres = getData(numSamples)
#dates, temps, hums = getData(6)
writeData(numSamples, dates, temps, hums, pres)
