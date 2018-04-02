from flask import Flask, render_template
import datetime
app = Flask(__name__)
@app.route("/")
def passData():
	tempfile = open("/home/pi/FourHundy/final/tempdata.txt","r")
	humfile = open("/home/pi/FourHundy/final/humdata.txt","r")
	pressfile = open("/home/pi/FourHundy/final/pressdata.txt","r")
	latestData = open("/home/pi/FourHundy/final/latestData.txt","r")
	
	info1 = tempfile.readlines() #Reads the data line by line
	info2 = humfile.readlines()
	info3 = pressfile.readlines()
	alerttime1 = info1[0].strip() #alerttime1 becomes the first line (date and time)
	alerttime2 = info2[0].strip()
	alerttime3 = info3[0].strip()
	temp = info1[1].strip() #temp becomes the second line (data)
	hum = info2[1].strip()
	press = info3[1].strip()
	
	latestInfo = latestData.readlines()
	currentdate = latestInfo[0].strip()
	currenttemp = latestInfo[0].strip()
	currenthum = latestInfo[0].strip()
	currentpres = latestInfo[0].strip()
	
	
	templateData = {
		'alerttime1' : alertime1,
		'alerttime2' : alertime2,
		'alerttime3' : alertime3,
		'alerttemp' : temp,
		'alerthum' : hum,
		'alertpress' : press,
		'time' : currentdate,
		'temp' : currenttemp,
		'hum' : currenthum,
		'press' : currentpres
		}
	tempfile.close()
	humfile.close()	
	pressfile.close()
	latestData.close()
	
	return render_template('index.html',** templateData)
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)