#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO

LEFT = 17
RIGHT = 27
DIR = 20									    # GPIO pin for Direction (Digital)
STEP = 18										# GPIO pin for Step Output (PWM)
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT, GPIO.IN)                      # 
GPIO.setup(RIGHT,GPIO.IN)                      # 
GPIO.setup(DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
GPIO.setup(STEP, GPIO.OUT)	                   # Initialization of Step Output Pin


while(1):

    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)
    print(left)



GPIO.cleanup()

	