#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

from time import sleep
import math

import rospy
from std_msgs.msg import String

class F_A_Publisher:
    def __init__(self,PGV_2_PGA, PGA):

        self.PGV_2_PGA = PGV_2_PGA
        self.PGA = PGA

        rospy.init_node('F_A_Publisher', anonymous=False)          # Initialization of Node
        self.pub1 = rospy.Publisher("F", Float64, queue_size=10)      
        self.pub2 = rospy.Publisher("A", Float64, queue_size=10)
        
        
    def F_A_Compute(self):

        self.F = 1 / (2 * math.pi * self.PGV_2_PGA)
        self.A = (9.807 * self.PGA) / (4 * math.pi**2 * self.F)
        self.publish_F_A()
        return self.F, self.A
        

    def publish_F_A(self):
        self.pub1. publish(self.F)
        self.pub2. publish(self.A)
        
            
class Velocity_Publisher:
    def __init__(self,F,A):

        self.Hz = 100
        self.F = F
        self.A = A      
        #rospy.init_node('F_A_Subscriber', anonymous=False)
        #rospy.Subscriber("F", Float64, self.callback_F, queue_size=100, buff_size=160*1024)
        #rospy.Subscriber("A", Float64, self.callback_A, queue_size=100, buff_size=160*1024)

        self.pub = rospy.Publisher("Velocity", Float64, queue_size=10)     # Publishing to the topic "Frequency"

        self.Publish_Velocity()

    def Publish_Velocity(self):
        self.rate = rospy.Rate(self.Hz)

        self.T = 1/self.F

        self.step_nm = int(self.T * self.Hz) + 1

        for self.j in range(self.step_nm):
            self.t = self.j / self.Hz
            self.velocity = 2 * math.pi * self.A * self.F * math.sin(2 * math.pi * self.F * self.t)
            self.pub.publish(self.velocity)
            #print("Pub:",self.velocity)

        self.pub.publish(0.0)
    # def callback_F(self, msg):
    #     self.F = msg.data
    # def callback_A(self, msg):
    #     self.A = msg.data



