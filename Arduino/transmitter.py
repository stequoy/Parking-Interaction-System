from periphery import GPIO
from time import sleep
trans = GPIO("/dev/gpiochip2", 13, "out")  # pin 37
while True:
 trans.write(True)
 sleep(0.01)
 trans.write(False)
 sleep(0.01)
 trans.write(True)
 sleep(0.01)
 trans.write(False)
 sleep(0.01)
 trans.write(True)
 sleep(0.01)
 trans.write(False)
 sleep(0.01)
