#See temp_alert.py for comments
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "testerino.spam12@gmail.com"
toaddr = "kirstycha@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Alert From Your Raspberry Pi Monitoring System"

body = "An Anomaly In Your Home's Humidity Has Been Detected. Please See The Attached File For Details"

msg.attach(MIMEText(body, 'plain'))

filename = "DataFile.txt" #add in later
attachment = open("/home/pi/FourHundy/final/DataFile.txt", "rb") #add in later

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "testerino")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
