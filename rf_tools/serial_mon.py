#!/usr/bin/env python
"""
serial_mon.py Serial Port Monitoring Tool for RF Sensors
---------------------------------------------------------------------------------
  Visit projects.privateeyepi.com for full details                                 
                                                                                  
 J. Evans November 2017
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V1.00 - Release
 -----------------------------------------------------------------------------------
"""
import sys
import serial
import time
from time import sleep
from math import log

baud = 115200                 # baud rate
port = '/dev/ttyAMA0'       # serial URF port on this computer

#-----------------

def serial_mon(baud):
	ser = serial.Serial(port, baud)
	ser.timeout = 0

	ser.flushInput()    # clear input buffer
	sys.stdout.flush()
	message=""
	cnt=0;
	while 1:
		if ser.inWaiting() > 0:
			char=ser.read(1)
			if char == 'a':
				sleep(0.01)
				message='a'+ser.read(11)
				now = time.strftime("%c")
				print time.strftime("%c") + " " + message;
				message= "";
				cnt=0;

if __name__ == "__main__":   # run the program from the command line
   import sys
   serial_mon(sys.argv[1])
