#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 18
CW = 1
CCW = 0
SPR = 2000  # no of steps 1600 = 1 Revolution Can be configured on the Driver

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR*10
#delay = .00001*5  #pulse width / Velocity

p = GPIO.PWM(STEP,1) #(Channel,Freq)
p.start(50) # pulse width percentage


def callback(data):
	#print(data.data)
	 
	if(data.data>=0):
		GPIO.output(DIR, CW)
	else:
		GPIO.output(DIR, CCW)
	
	if(abs(data.data)>0):
		p.ChangeFrequency(abs(data.data)) 
		#print(data.data)
	
	if(data.data)==4001: #Maximum Frequency is 4000KHz = 1200 RPM
		p.stop()
		rospy.loginfo("Ending Motion")
		rospy.signal_shutdown("Stopping")
  		  
	#GPIO.output(STEP, GPIO.HIGH)
	#sleep(abs(data.data))
	#GPIO.output(STEP, GPIO.LOW)
	#sleep(abs(data.data))
	

def motorcnt():
	
	
	rospy.init_node('Freq_listener', anonymous=True)

	rospy.Subscriber("Frequency", Float64, callback, queue_size=100, buff_size=160*1024)
	
	if rospy.is_shutdown():
		exit()
	rospy.spin()



if __name__ == '__main__':
	motorcnt()
	
GPIO.cleanup()
