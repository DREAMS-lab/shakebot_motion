#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO
import csv


class Motor_Calibrator: 

    def __init__(self):   

        self.file = open('Parameters.csv')
        type(self.file)
        self.csvreader = csv.reader(self.file)
        self.rows=[]
        for row in self.csvreader:
                self.rows.append(row)
                
        self.CW = 1
        self.CCW = 0
                
        for i in range(0,len(self.rows)):
            if(self.rows[i][0]=="LEFT"):
                self.LEFT = int(self.rows[i][1])
            if(self.rows[i][0]=="RIGHT"):
                self.RIGHT = int(self.rows[i][1])
            if(self.rows[i][0]=="DIR"):
                self.DIR = int(self.rows[i][1])
            if(self.rows[i][0]=="STEP"):
                self.STEP = int(self.rows[i][1])
            if(self.rows[i][0]=="Hub_Diameter"):
                self.hub_dia = float(self.rows[i][1])
            if(self.rows[i][0]=="Step_angle"):
                self.step_angle = float(self.rows[i][1])

        self.file.close()

        self.total_steps = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT, GPIO.IN)                     # Initialize the LEFT GPIO as an input for left limit switch
        GPIO.setup(self.RIGHT,GPIO.IN)                     # Initialize the RIGHT GPIO as an input for right limit switch
        GPIO.setup(self.DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
        GPIO.setup(self.STEP, GPIO.OUT)	                   # Initialization of Step Output Pin
        self.delay = 0.001
        
        #self.ls_checker()

        self.calibrate()

        for i in range(0,len(self.rows)):
            if(self.rows[i][0]=="Total_Steps"):
                self.rows[i][1] = self.total_steps

        self.file = open('Parameters.csv','w')             # To update the total steps in the csv file
        self.writer = csv.writer(self.file)
        for i in range(0,len(self.rows)):
                self.writer.writerow(self.rows[i])
        self.file.close()
        
    def ls_checker(self):
        while(1):
            self.left = GPIO.input(self.LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            print(self.left,self.right)


    def calibrate(self):
        
        self.steps = 0
        self.left = GPIO.input(self.LEFT)                                        
        self.right = GPIO.input(self.RIGHT)

        
        while(self.left==0):                               # To translate the bed to the left end
            GPIO.output(self.DIR,self.CCW)
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
            self.left = GPIO.input(self.LEFT)                                        
            #right = GPIO.input(RIGHT)

        sleep(1)
        
        while(self.right==0):                              # To translate the bed to the right end
            GPIO.output(self.DIR, self.CW)
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
            #left = GPIO.input(LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            self.steps = self.steps+1
        
        self.total_steps = self.steps
        self.position = int(input("Enter Desired Position of Bed (in %) :"))

        self.desired_step = int(self.steps * (self.position / 100))

        GPIO.output(self.DIR,self.CCW)
        while not (self.steps==self.desired_step):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
            self.left = GPIO.input(self.LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            self.steps = self.steps-1

if __name__ == '__main__':
        
    motor_1 = Motor_Calibrator()
    GPIO.cleanup()

	