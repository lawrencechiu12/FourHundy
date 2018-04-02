import sqlite3
import time
import sys
#import time

num = 2
old_dict = {'dates': None, 'temp': None, 'hum': None, 'pres': None}
#old_dict = {'dates': None, 'temp': None, 'hum': None}
new_dict = {'dates': None, 'temp': None, 'hum': None, 'pres': None}
#new_dict = {'dates': None, 'temp': None, 'hum': None}

def getData(num):
	conn = sqlite3.connect('sensorsData.db')
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY time_UTC DESC LIMIT "+str(num))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	pres = []
	conn.close()
	for row in reversed(data):
		dates.append(row[1])
		hums.append(row[2])
		temps.append(row[3])
		pres.append(row[4])

	return dates, temps, hums, pres
	#return dates, temps, hums


def compareData(dates, temps, hums, pres):
#def compareData(dates, temps, hums):
tempfile = open("/home/pi/FourHundy/final/tempdata.txt","w+")
humfile = open("/home/pi/FourHundy/final/humdata.txt","w+")
pressfile = open("/home/pi/FourHundy/final/pressdata.txt","w+")
	import database_filewrite
	if abs(temps[0] - temps[1]) > 4:
		print "temp"
		tempfile.write((str(dates[1])) + "\n" + (str(temps[1])) + "\n") # will write the latest data(the data the caused the alert) and time to a file
		#sudo python /home/pi/FourHundy/final/Scripts/temp_alert.py
		import temp_alert
		tempfile.close()
	if abs(hums[0] - hums[1]) > 5:
		print "hums"
		humfile.write((str(dates[1])) + "\n" + (str(hums[1])) + "\n")# will write the latest data(the data the caused the alert) and time to a file
		#sudo python /home/pi/FourHundy/final/Scripts/hum_alert.py
		import hum_alert
		humfile.close()
	if abs(pres[0] - pres[1]) > 5:
		print "pres"
		pressfile.write((str(dates[1])) + "\n" + (str(press[1])) + "\n")# will write the latest data(the data the caused the alert) and time to a file
		#sudo python /home/pi/FourHundy/final/Scripts/pres_alert.py
		import pres_alert
		pressfile.close()
	else:
		print "no alert"
		tempfile.close()
		humfile.close()
		pressfile.close()

#while True:
dates, temps, hums, pres = getData(num)
#dates, temps, hums = getData(num)
#compareData(dates,temps,hums)
compareData(dates,temps,hums,pres)
#time.sleep(600) #Happens everytime data is taken
