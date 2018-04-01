#!/usr/bin/env python

import sys
import serial
from time import sleep
from math import log

baud = 9600                 # baud rate
port = '/dev/ttyAMA0'       # serial URF port on this computer

ser = serial.Serial(port, baud)
ser.timeout = 0

def request(device, request, retry):
    # sends a message to 'device' with content 'request'
    # returns 'response' from from device
    # retries a number of times, pausing longer between retries each time round

	n = 0
	while (n < retry):
		#sleep(n)            # sleep longer each time I don't get a response
		ser.flushInput()    # clear input buffer
		if verbatim:
			print ('sending     :' + request)
			ser.write(request)  # see if our device is online
		else:
			print ('sending     : a' + device + request)
			ser.write('a' + device + request)  # see if our device is online
		timeout=15;
		while ser.inWaiting() == 0 and timeout!=0:
			sleep(0.05)
			timeout = timeout - 1
		if timeout==0:
				response="No response"
		else:
			sys.stdout.write( "response is : ")
			while ser.inWaiting():
				sys.stdout.write(ser.read(1))
				sleep(0.01)
				n=retry
		n = n + 1
	print ""
	return


def getstarted(devid):      # wait for the STARTED message from devid
    t = 1
    while t == 1:
        if ser.inWaiting() >=12:
            if ser.read() == 'a':   # llap message start
                message = 'a'
                if ser.read(2) == devid:    # message is from our device
                    if ser.read(9) == 'STARTED--':  # devid has started
                        t = 0
        ser.flushInput()
        sleep(1)
    return()

def commandsensor(devid, command):
	# send a command to a device
	request(devid,command,3)
	exit()

if __name__ == "__main__":   # run the program from the command line
	import sys
	verbatim=0
	if (sys.argv[2]=="-V" or sys.argv[2]=="-v"):
		verbatim=1
		commandsensor("",sys.argv[1])
	else:
		commandsensor(sys.argv[1],sys.argv[2])
