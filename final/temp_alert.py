import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "testerino.spam12@gmail.com" #Sender email
toaddr = "testerino.spam12@gmail.com" #Recieving email

msg = MIMEMultipart()

#To, From, and Subject Line of the Email
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Alert From Your Raspberry Pi Monitoring System"

#Email Message
body = "An Anomaly In Your Home's Temperature Has Been Detected. Please See The Attached File For Details"

msg.attach(MIMEText(body, 'plain'))

#Configuring the attachment
filename = "DataFile.txt" #Name of the file to be sent
attachment = open("/home/pi/FourHundy/final/DataFile.txt", "rb") # Pathway to the file to be sent

#Attaching the attachment to the email
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

#Info on the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "testerino")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
