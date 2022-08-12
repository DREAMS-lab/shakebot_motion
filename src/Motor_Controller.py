#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
import math
from time import sleep
import RPi.GPIO as GPIO
import csv

class motor_controller:
    def __init__(self):
        self.file = open('Parameters.csv')
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

        self.file.close()
        self.hub_dia = self.hub_dia/1000

        GPIO.setmode(GPIO.BCM)						   # Initialization of GPIO pins in BCM(Broadcom SOC mode) 
        GPIO.setup(self.DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
        GPIO.setup(self.STEP, GPIO.OUT)					   # Initialization of Step Output Pin

        self.p = GPIO.PWM(self.STEP,1) 						   # Initializing the GPIO pin to output PWM signal
        self.p.start(50) 

    def motorcnt(self):
        rospy.init_node('Velocity_Subscriber', anonymous=True)	# Initialization of Node
        rospy.Subscriber("Velocity", Float64, self.callback1, queue_size=100, buff_size=160*1024)
        if rospy.is_shutdown():
            exit()  
        rospy.spin()

    def callback1(self,data):
        #print(self.data.data)
        self.hub_dia
        
        self.linear_vel = self.data.data
        
        self.speed_rpm = self.linear_vel * 60 / (self.hub_dia/2)  / (2*math.pi)                 # Revolutions per Minute || Angular Velocity = Linear Velocity / Radius of Hub

        self.pulse_per_sec = self.speed_rpm  / ((self.step_angle/360) * 60)      # Pulses per Second = RPM * 360 * 360 / (Pulse/Rev * 60)
        
        self.freq_max = 20 * self.pulse_per_sec

        if(self.freq_max>=0):						   # Condition to check the direciton of motor
            GPIO.output(self.DIR, self.CW)
        else:
            GPIO.output(self.DIR, self.CCW)
        
        if(abs(self.freq_max)>0 and abs(self.freq_max)!=0.0):					   # To Publish the frequency of motor through the GPIO pin
            self.p.ChangeFrequency(abs(self.freq_max)) 
            #print(self.data.data)
        
        elif(abs(self.freq_max)==0.0):           # To stop the motor upon completion of the motion
            self.p.ChangeFrequency(0.0)
        
        if(self.speed_rpm)>=1200: 					   
            rospy.loginfo("Speed is too high...! Exiting...!")
            rospy.signal_shutdown("Stopping")


if __name__ == '__main__':

    motor1 = motor_controller()

    motor1.motorcnt()

    GPIO.cleanup()
