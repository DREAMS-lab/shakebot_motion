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
        self.A = (self.PGA) / (4 * math.pi**2 * self.F**2)
        self.publish_F_A()
        return self.F, self.A
        

    def publish_F_A(self):
        self.pub1. publish(self.F)
        self.pub2. publish(self.A)
        
            
class Velocity_Publisher:
    def __init__(self,F,A):

        self.Hz = 200
        self.F = F
        self.A = A      
        #rospy.init_node('F_A_Subscriber', anonymous=False)
        #rospy.Subscriber("F", Float64, self.callback_F, queue_size=100, buff_size=160*1024)
        #rospy.Subscriber("A", Float64, self.callback_A, queue_size=100, buff_size=160*1024)

        self.pub = rospy.Publisher("Velocity", Float64, queue_size=10)     # Publishing to the topic "Frequency"
        self.csv_read()

        self.Publish_Velocity()

    def csv_read(self):
        self.file_read = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Parameters.csv')
        type(self.file_read)
        self.csvreader = csv.reader(self.file_read)
        self.rows=[]
        for row in self.csvreader:
                self.rows.append(row)
        self.file_read.close()

        for i in range(0,len(self.rows)):
            if(self.rows[i][0]=="Velocity_Multiplier"):
                self.multiplier = self.rows[i][1]

    def Publish_Velocity(self):
        self.rate = rospy.Rate(self.Hz)

        self.T = 1/self.F

        self.step_nm = int(self.T * self.Hz) + 1
        
        #print(self.step_nm)

        self.j = 0
        
        for self.j in range(self.step_nm):
            self.t = self.j / self.Hz
            self.velocity = 2 * math.pi * self.A * self.F * math.sin(2 * math.pi * self.F * self.t)
            self.velocity = self.velocity * float(self.multiplier)
            self.pub.publish(self.velocity)
            #rospy.loginfo(self.velocity)
            self.rate.sleep()
            #print("t:",self.t," velocity:",self.velocity)  #," F:",self.F," A:",self.A)
        

        self.pub.publish(0.0)
    # def callback_F(self, msg):
    #     self.F = msg.data
    # def callback_A(self, msg):
    #     self.A = msg.data



