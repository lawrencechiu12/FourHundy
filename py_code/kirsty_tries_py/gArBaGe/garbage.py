import serial
ser = serial.Serial('/dev/ttyACM0',9600)

while True:
    read_serial=ser.readline()
    read_in_string=read_serial.decode("utf-8")
    print(read_in_string)
