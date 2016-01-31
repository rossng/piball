import time
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(int(sys.argv[1]))
'''
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
'''
time.sleep(5)
p.stop()
GPIO.cleanup()