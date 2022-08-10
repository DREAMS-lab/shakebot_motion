#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
import math
from time import sleep
import RPi.GPIO as GPIO
import csv

DIR = 20									    # GPIO pin for Direction (Digital)
STEP = 18										# GPIO pin for Step Output (PWM)
CW = 1
CCW = 0
hub_dia = 51.812
step_angle = 1.8


GPIO.setmode(GPIO.BCM)						   # Initialization of GPIO pins in BCM(Broadcom SOC mode) 
GPIO.setup(DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
GPIO.setup(STEP, GPIO.OUT)					   # Initialization of Step Output Pin

p = GPIO.PWM(STEP,1) 						   # Initializing the GPIO pin to output PWM signal
p.start(50)  

def callback(data):

    linear_vel = data.data
    
    hub_dia = hub_dia / 1000                                     # Pulley With Belt 48.51mm (Pulley Diameter) + 2 * 1.651mm (Thickness of Belt)= 51.812mm
    
    speed_rpm = linear_vel * 60 / (hub_dia/2)  / (2*math.pi)                 # Revolutions per Minute || Angular Velocity = Linear Velocity / Radius of Hub

    pulse_per_sec = speed_rpm  / ((step_angle/360) * 60)      # Pulses per Second = RPM * 360 * 360 / (Pulse/Rev * 60)
    
    freq_max = 20 * pulse_per_sec

    if(freq_max>=0):						   # Condition to check the direciton of motor
        GPIO.output(DIR, CW)
    else:
        GPIO.output(DIR, CCW)
	
    if(abs(freq_max)>0 and abs(freq_max)!=4001):					   # To Publish the frequency of motor through the GPIO pin
        p.ChangeFrequency(abs(freq_max)) 
		#print(data.data)
	
    if(speed_rpm)>=1200: 					   # To stop the motor upon completion of the motion
        rospy.loginfo("Speed is too high...! Exiting...!")
        rospy.signal_shutdown("Stopping")

def callback2(data):
    if(data.data==1):
        rospy.loginfo("Ending Motion")
        rospy.signal_shutdown("Stopping")
        

def motorcnt():
	
    rospy.init_node('Velocity_Subscriber', anonymous=True)	# Initialization of Node
    rospy.Subscriber("Velocity", Float64, callback, queue_size=100, buff_size=160*1024)  # Subscribing to the topic "Frequency"
    rospy.Subscriber("Motion_Status", int, callback2)  # Subscribing to the topic "Frequency"

    if rospy.is_shutdown():
        exit()  
    rospy.spin()



if __name__ == '__main__':
    
    file = open('Parameters.csv')
    type(file)
    csvreader = csv.reader(file)
    rows=[]
    for row in csvreader:
        rows.append(row)

    for i in range(0,len(rows)):
        if(rows[i][0]=="LEFT"):
            LEFT = rows[i][1]
        if(rows[i][0]=="RIGHT"):
            RIGHT = rows[i][1]
        if(rows[i][0]=="DIR"):
            DIR = rows[i][1]
        if(rows[i][0]=="STEP"):
            STEP = rows[i][1]
        if(rows[i][0]=="Hub_Diameter"):
            hub_dia = rows[i][1]
        if(rows[i][0]=="Step_angle"):
            step_angle = rows[i][1]

    print(LEFT,RIGHT,DIR,STEP,hub_dia,step_angle)

    motorcnt()
    file.close()
    GPIO.cleanup()							   # Cleanup of GPIO pins whilst exiting the program