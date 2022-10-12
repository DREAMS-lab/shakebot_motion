#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO
import csv
import os
import time

import rospy
from shakebot_motion.msg import calib_msg


class Motor_Positioner: 

    def __init__(self):   
        GPIO.setwarnings(False)

        self.CW = 1
        self.CCW = 0
        ############################ Publishing Parameters ########################################
        self.left = 0
        self.right = 0
        self.position = 0
        self.rail_length = 0
        ###########################################################################################
        self.csv_read()

        rospy.init_node('Bed_April_Tag_Calibrator', anonymous=True)
        self.pub = rospy.Publisher('calibration_parameters', calib_msg, queue_size=10)
    
        os.system('clear')

        print("Please find the following Default Parameters and confirm them")

        print("LEFT Limitswitch PIN :",self.LEFT,"\nRIGHT Limitswitch PIN :",self.RIGHT,"\nDIR PIN :",self.DIR,"\nSTEP PIN :",self.STEP,"\nHub Diameter :",self.hub_dia,"\nStep Angle :",self.step_angle,"\nRail Length :",self.rail_length)

        print("Press Y to confirm Parameter Values or N to change them")
        self.parameter_confirmation = input()

        if(self.parameter_confirmation=='N'):
            self.csv_edit()
            self.csv_write()
            os.system('clear')
            print("Parameters Updated")
        else:
            os.system('clear')
            print("Proceeding with Default Parameters")

        print("Starting Calibration")
        self.total_steps = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT, GPIO.IN)                     # Initialize the LEFT GPIO as an input for left limit switch
        GPIO.setup(self.RIGHT,GPIO.IN)                     # Initialize the RIGHT GPIO as an input for right limit switch
        GPIO.setup(self.DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
        GPIO.setup(self.STEP, GPIO.OUT)	                   # Initialization of Step Output Pin
        self.delay = 0.001

        self.calibrate()
        #self.test()
        
        self.csv_write()
        
        os.system('clear')
        print("Calibration Complete")
        sleep(1.5)
        print("Exiting")
        
        GPIO.cleanup()
    
    def test(self):
        while(1):
            self.left = GPIO.input(self.LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            print(self.left,self.right)
            
    def csv_read(self):
        self.file = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Parameters.csv')
        type(self.file)
        self.csvreader = csv.reader(self.file)
        self.rows=[]
        for row in self.csvreader:
                self.rows.append(row)
                
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
            if(self.rows[i][0]=="Rail_Length"):
                self.rail_length = float(self.rows[i][1])
            if(self.rows[i][0]=="Total_Steps"):
                self.total_steps = float(self.rows[i][1])
                

        self.file.close()

    def csv_edit(self):
        print("Please enter number to update the parameter:")
        print("1.LEFT,2.RIGHT,3.DIR,4.STEP,5.Hub_Diameter,6.Step_angle,7.Rail_Length,")
        self.parameter_number = int(input())
        
        if(self.parameter_number==1):
            print("Please enter the new LEFT PIN")
            self.LEFT = int(input())
        elif(self.parameter_number==2):
            print("Please enter the new RIGHT PIN")
            self.RIGHT = int(input())
        elif(self.parameter_number==3):
            print("Please enter the new DIR PIN")
            self.DIR = int(input())
        elif(self.parameter_number==4):
            print("Please enter the new STEP PIN")
            self.STEP = int(input())
        elif(self.parameter_number==5):
            print("Please enter the new Hub Diameter")
            self.hub_dia = float(input())
        elif(self.parameter_number==6):
            print("Please enter the new Step Angle")
            self.step_angle = float(input())
        elif(self.parameter_number==7):
            print("Please enter the new Rail Length")
            self.rail_length = float(input())
        else:
            print("Invalid Input")
            self.csv_edit()

        print("Do you want to edit more parameters? Y/N")
        self.edit_check = input()
        if(self.edit_check=='Y'):
            self.csv_edit()
        

    def csv_write(self):

        for i in range(0,len(self.rows)):
            if(self.rows[i][0]=="LEFT"):
                self.rows[i][1] = self.LEFT
            if(self.rows[i][0]=="RIGHT"):
                 self.rows[i][1] = self.RIGHT
            if(self.rows[i][0]=="DIR"):
                 self.rows[i][1] = self.DIR
            if(self.rows[i][0]=="STEP"):
                 self.rows[i][1] = self.STEP
            if(self.rows[i][0]=="Hub_Diameter"):
                 self.rows[i][1] = self.hub_dia
            if(self.rows[i][0]=="Step_angle"):
                self.rows[i][1] = self.step_angle
            if(self.rows[i][0]=="Rail_Length"):
                self.rows[i][1] = self.rail_length
            if(self.rows[i][0]=="Total_Steps"):
                self.rows[i][1] = self.total_steps
            if(self.rows[i][0]=="Distance_Unit_Step"):
                self.rows[i][1] = self.rail_length/self.total_steps

        self.file_write = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Parameters.csv','w')             # To update the total steps in the csv file
        self.writer = csv.writer(self.file_write)
        for i in range(0,len(self.rows)):
            self.writer.writerow(self.rows[i])
        self.file_write.close()

    def publish_data(self):
        msg = calib_msg()
        msg.left_ls = self.left
        msg.right_ls = self.right
        msg.bed_length = self.rail_length
        msg.bed_position = self.position    # Publish the user defined position in mm
        self.pub.publish(msg)

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
            self.right = GPIO.input(self.RIGHT)
            self.publish_data()
            
        sleep(1)
        
        while(self.right==0):                              # To translate the bed to the right end
            GPIO.output(self.DIR, self.CW)
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
            self.left = GPIO.input(self.LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            self.steps = self.steps+1
            self.publish_data()
        
        self.total_steps = self.steps

        print("Enter the distance from left end to position the bed (in mm):")
        self.position = float(input())
        self.desired_step = int((self.position/self.rail_length)*self.total_steps)

        GPIO.output(self.DIR,self.CCW)
        while not (self.steps==self.desired_step):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
            self.left = GPIO.input(self.LEFT)                                        
            self.right = GPIO.input(self.RIGHT)
            self.steps = self.steps-1

        tic = time.time()
        while(tock-tic<2):
            tock = time.time()
            self.publish_data()
            time.sleep(0.1)
        

        print("Bed Positioned at ",self.position," mm from left end")

if __name__ == '__main__':
        
    motor_1 = Motor_Positioner()
    

	
