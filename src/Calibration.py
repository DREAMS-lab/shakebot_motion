#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO
import csv

LEFT = 27
RIGHT = 17
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

def calibrate():
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
        print(right)
        
    position = int(input("Enter Desired Position of Bed (in %) :"))

    desired_step = int(steps * (position / 100))

    GPIO.output(DIR,CCW)
    while not (steps==desired_step):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        left = GPIO.input(LEFT)                                        
        right = GPIO.input(RIGHT)
        steps = steps-1

if __name__ == '__main__':
    
    # while(1):
    
    #     left = GPIO.input(LEFT)                                        
    #     right = GPIO.input(RIGHT)
        
    #     print("Left",left)
    #     print("Right",right)  
    #     print("\n")  
        
    #     GPIO.output(STEP, GPIO.HIGH)
    #     sleep(delay)
    #     GPIO.output(STEP, GPIO.LOW)
    #     sleep(delay)
        
    #     if(right == 1 or left == 1):
    #         break

    file = open('Parameters.csv')
    type(file)
    csvreader = csv.reader(file)
    rows=[]
    for row in csvreader:
        rows.append(row)

    for i in range(0,len(rows)):
        if(rows[i][0]=="LEFT"):
            LEFT = int(rows[i][1])
        if(rows[i][0]=="RIGHT"):
            RIGHT = int(rows[i][1])
        if(rows[i][0]=="DIR"):
            DIR = int(rows[i][1])
        if(rows[i][0]=="STEP"):
            STEP = int(rows[i][1])
        if(rows[i][0]=="Hub_Diameter"):
            hub_dia = rows[i][1]
        if(rows[i][0]=="step_angle"):
            step_angle = rows[i][1]
    
    calibrate()
    GPIO.cleanup()

	