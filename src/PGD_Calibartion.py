
import rospy

import time
from datetime import datetime
import csv
import os
from std_msgs.msg import Float64
import math
import numpy as np
import matplotlib.pyplot as plt


class PGD_Calibrate():
        def __init__(self):

            print("Enter Peak Ground Velocity / Peak Ground Acceleration Ratio:")
            self.PGV_2_PGA = float(input())
            print("Enter Peak Ground Acceleration(Gs):")
            self.PGA = float(input())

            self.PGA = self.PGA * 9.80665   # Converting to m/s^2
        
            print("Initiating Rock Shaking")
            time.sleep(1)
            
            self.F_A = F_A_Publisher(self.PGV_2_PGA,self.PGA)
            
            self.F, self.A = self.F_A.F_A_Compute()
            
            self.Velocity_Publisher = Velocity_Publisher(self.F,self.A)


class Velocity_Publisher:
    def __init__(self,F,A):

        self.Hz = 200
        self.F = F
        self.A = A      
        #rospy.init_node('F_A_Subscriber', anonymous=False)
        #rospy.Subscriber("F", Float64, self.callback_F, queue_size=100, buff_size=160*1024)
        #rospy.Subscriber("A", Float64, self.callback_A, queue_size=100, buff_size=160*1024)

        self.pub = rospy.Publisher("/data_acquisition/Velocity", Float64, queue_size=10)     # Publishing to the topic "Frequency"

        self.Publish_Velocity()

    def Publish_Velocity(self):
        self.rate = rospy.Rate(self.Hz)

        self.T = 1/self.F

        self.step_nm = int((self.T * self.Hz)/2) + 1
        
        #print(self.step_nm)

        self.j = 0
        
        self.displacement = 0.0
        self.disp = 0.0

        # disp = np.zeros(self.step_nm)
        # vel = np.zeros(self.step_nm)
        # t = np.array(range(self.step_nm))
        # t = t/self.Hz

        for self.j in range(self.step_nm):
            self.t = self.j / self.Hz
            self.velocity = 2 * math.pi * self.A * self.F * math.sin(2 * math.pi * self.F * self.t)
            self.pub.publish(self.velocity)
            #rospy.loginfo(self.velocity)
            self.rate.sleep()
            #print("t:",self.t," velocity:",self.velocity)  #," F:",self.F," A:",self.A)
            self.disp = (-self.A*math.cos(2*math.pi*self.F*self.t)) + self.A
            self.disp = self.disp
            #disp[self.j] = self.disp
            #vel[self.j] = self.velocity
            
        self.pub.publish(0.0)

        # plt.plot(t,vel)
        # plt.plot(t,disp)
        # plt.legend(['Velocity','Displacement'])
        # plt.show()

        print("The Computed Displacement is: ",round(self.disp*100,2)," cms")


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

if __name__ == '__main__':
        
        User_Interface = PGD_Calibrate()