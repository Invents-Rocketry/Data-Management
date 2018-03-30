#!/usr/bin/python

import Adafruit_BBIO.PWM as PWM
import time

servoA = "P8_13"
#servoB = "P8_19"
#servoC = "P9_14"
PWM.start(servoA, 0, 1000)
for i in range(1,6):
    DC = 100/i 
    #DC = V/3.365
    #   if DC > 100:
    #       DC = 100
    PWM.set_duty_cycle(servoA, DC)
    time.sleep(5)
PWM.stop(servoA)
#PWM.stop(servoB)
#PWM.stop(servoC)
PWM.cleanup()
