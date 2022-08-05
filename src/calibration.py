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

p = GPIO.PWM(STEP,1) 						   # Initializing the GPIO pin to output PWM signal
p.start(50)  								   # Starting the motor with 50% duty cycle

left_steps = 0
left = GPIO.input(LEFT)                                        
right = GPIO.input(RIGHT)

while(left==0):
    GPIO.output(DIR, CW)
    p.ChangeFrequency(2457.4221)               # Velocity Capped at 0.1 m/s
    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)
    left_step = step+1

p.ChangeDutyCycle(0)

while(right==0):
    GPIO.output(DIR, CCW)
    p.ChangeFrequency(2457.4221)               # Velocity Capped at 0.1 m/s
    p.ChangeDutyCycle(50)
    left = GPIO.input(LEFT)                                        
    right = GPIO.input(RIGHT)
    right_step = step+1
    



GPIO.cleanup()

	