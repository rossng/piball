import serial
ser = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)  # open first serial port
print(ser.portstr)       # check which port was really used
ser.write("hello".encode('latin-1'))      # write a string
ser.close()             # close port