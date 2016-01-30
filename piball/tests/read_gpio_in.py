import RPi.GPIO as GPIO
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN)

while True:
    time.sleep(0.5)
    if GPIO.input(16):
        print('high')
    else:
        print('low')