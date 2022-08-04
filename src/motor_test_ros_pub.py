#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep

import rospy
from std_msgs.msg import String
import math

def talker():
    pub = rospy.Publisher('Frequency', Float64, queue_size=10)      # Publishing to the topic "Frequency"
    rospy.init_node('Freq_Publisher', anonymous=True)               # Initialization of Node
    rate = rospy.Rate(200)                                          # Rate of publishing the data
    
    T = 200
    t=0

    linear_vel = float(input("Enter the linear velocity: "))

    pulse_rev = 2000                                            # Number of pulses per revolution
    
    hub_dia = 51.812 / 1000                                     # Pulley With Belt 48.51mm (Pulley Diameter) + 2 * 1.651mm (Thickness of Belt)= 51.812mm
    
    speed_rpm = linear_vel * 60 / (hub_dia/2)  / (2*math.pi)                 # Revolutions per Minute || Angular Velocity = Linear Velocity / Radius of Hub

    # if(speed_rpm>1200):
    #     rospy.loginfo("Speed is too high...! Exiting...!")
    #     exit()
    
    freq_max = speed_rpm  / ((1.8/360) * 60)      # Frequency = RPM * 360 * 360 / (Pulse/Rev * 60)
    
    rospy.loginfo(speed_rpm)
    rospy.loginfo(freq_max)
    
    while not rospy.is_shutdown():
        if t < T:
            freq = round((freq_max*math.sin(t/T*2*math.pi)),4)
            #rospy.loginfo(freq)
            t=t+1
            pub.publish(freq)
        rate.sleep()
        
        if(t==T):
            pub.publish(4001)
            rospy.loginfo("Reached End of Motion")
            exit()

if __name__ == '__main__':
        talker()

