#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep
import RPi.GPIO as GPIO

DIR = 20									    # GPIO pin for Direction (Digital)
STEP = 18										# GPIO pin for Step Output (PWM)
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)						   # Initialization of GPIO pins in BCM(Broadcom SOC mode) 
GPIO.setup(DIR, GPIO.OUT)					   # Initialization of Direction Output Pin
GPIO.setup(STEP, GPIO.OUT)					   # Initialization of Step Output Pin

p = GPIO.PWM(STEP,1) 						   # Initializing the GPIO pin to output PWM signal
p.start(50)  								   # Starting the motor with 100% duty cycle	


def callback(data):
	#print(data.data)						   # Used to print the data received
 
	if(data.data>=0):						   # Condition to check the direciton of motor
		GPIO.output(DIR, CW)
	else:
		GPIO.output(DIR, CCW)
	
	if(abs(data.data)>0 and abs(data.data)!=4001):					   # To Publish the frequency of motor through the GPIO pin
		p.ChangeFrequency(abs(data.data)) 
		#print(data.data)
	
	if(data.data)==4001: 					   # To stop the motor upon completion of the motion
		rospy.loginfo("Ending Motion")
		rospy.signal_shutdown("Stopping")

  		  


def motorcnt():
	
	
	rospy.init_node('Freq_listener', anonymous=True)	# Initialization of Node

	rospy.Subscriber("Frequency", Float64, callback, queue_size=100, buff_size=160*1024)  # Subscribing to the topic "Frequency"
	
	if rospy.is_shutdown():
		exit()
	rospy.spin()



if __name__ == '__main__':
	motorcnt()
	
GPIO.cleanup()							   # Cleanup of GPIO pins whilst exiting the program
