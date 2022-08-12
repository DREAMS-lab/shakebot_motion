#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep
import math

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('Velocity_Publisher', anonymous=True)          # Initialization of Node
    pub1 = rospy.Publisher("Velocity", Float64, queue_size=10)      # Publishing to the topic "Frequency"
    
    rate = rospy.Rate(200)                                         # Rate of publishing the data
    
    pub2.publish(0)
    velocity_max = 0.1

    t=0
    T=500
    
    while not rospy.is_shutdown():
        if t < T:
            t=t+1
            velocity = round((velocity_max*math.sin(t/T*2*math.pi)),4)
            pub1.publish(velocity)
        rate.sleep()
        
        if (t==T):
            t=0
            # pub1.publish(0.0)
            # rospy.loginfo("Reached End of Motion")
            # exit()
    
    
if __name__ == '__main__':
        talker()