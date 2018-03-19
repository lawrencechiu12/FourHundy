import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM) # This is setting the GPIO using the BCM chip
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Using GPIO21 (Pin 40)

#Set up our function that sends the OS command of shutdown
def Shutdown(channel):
	os.system("sudo shutdown -h now")

# Do the function when signal is sent (button pressed)
GPIO.add_event_detect(21, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)

#Wait forever until
while 1:
	time.sleep(1)
