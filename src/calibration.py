#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO

LEFT = 17
RIGHT = 13
DIR = 20									    # GPIO pin for Direction (Digital)
STEP = 18										# GPIO pin for Step Output (PWM)
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT, GPIO.IN)                      # 
GPIO.setup(RIGHT,GPIO.IN)                      # 
GPIO.setup(DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
GPIO.setup(STEP, GPIO.OUT)	                   # Initialization of Step Output Pin
delay = 0.001

steps = 0
left = GPIO.input(LEFT)                                        
right = GPIO.input(RIGHT)

GPIO.output(DIR,CCW)
while(left==0):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)

GPIO.output(DIR, CW)
while(right==0):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)
    steps = steps+1
    
position = int(input("Enter Desired Position of Bed (in %) :"))

desired_step = int(steps * (position / 100))

GPIO.output(DIR,CCW)
while(steps==desired_step):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)
    steps = steps-1


GPIO.cleanup()

	