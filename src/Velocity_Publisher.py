#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('Velocity_Publisher', anonymous=True)          # Initialization of Node
    pub1 = rospy.Publisher('Velocity', Float64, queue_size=10)      # Publishing to the topic "Frequency"
    pub2 = rospy.Publisher('Motion_Status', int, queue_size=10)     # Publishing to the topic "Frequency"
    rate = rospy.Rate(200)                                         # Rate of publishing the data
    
    pub2.publish(0)
    velocity = 0.1

    tim = 1
    while not rospy.is_shutdown():
        pub1.publish(velocity)
        sleep(tim)
    
    pub2.publish(1)

if __name__ == '__main__':
        talker()