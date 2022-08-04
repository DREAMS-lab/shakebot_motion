#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 18
CW = 1
CCW = 0
SPR = 2000  								  # No of Pulse need for 1 Revolution

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

p = GPIO.PWM(STEP,1) 						  # Initializing the GPIO pin to output PWM signal
p.start(100)  								  # Starting the motor with 100% duty cycle	


def callback(data):
	#print(data.data)						   # Used to print the data received
 
	if(data.data>=0):						   # Condition to check the direciton of motor
		GPIO.output(DIR, CW)
	else:
		GPIO.output(DIR, CCW)
	
	if(abs(data.data)>0):					   # To Publish the frequency of motor through the GPIO pin
		p.ChangeFrequency(abs(data.data)) 
		#print(data.data)
	
	if(data.data)==4001: 						# To stop the motor upon completion of the motion
		rospy.loginfo("Ending Motion")
		rospy.signal_shutdown("Stopping")

	if(abs(data.data)>4000):					# Safety Check to avoid overspeed or motor failure
		rospy.loginfo("Speed is too high")
		rospy.signal_shutdown("Ending Program")

  		  


def motorcnt():
	
	
	rospy.init_node('Freq_listener', anonymous=True)

	rospy.Subscriber("Frequency", Float64, callback, queue_size=100, buff_size=160*1024)
	
	if rospy.is_shutdown():
		exit()
	rospy.spin()



if __name__ == '__main__':
	motorcnt()
	
GPIO.cleanup()
