#!/usr/bin/env python3
import rospy

import time
from datetime import datetime
import csv
import os
from std_msgs.msg import Float64
import math
import numpy as np
import matplotlib.pyplot as plt
from shakebot_motion.msg import calib_msg


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
        
        self.velocity_multiplier = Velocity_Publisher(self.F,self.A)

class Velocity_Publisher:
    def __init__(self,F,A):

        self.Hz = 200
        self.F = F
        self.A = A      
        #rospy.init_node('F_A_Subscriber', anonymous=False)
        #rospy.Subscriber("F", Float64, self.callback_F, queue_size=100, buff_size=160*1024)
        #rospy.Subscriber("A", Float64, self.callback_A, queue_size=100, buff_size=160*1024)
        
        #rospy.init_node('PGD_Calibrator', anonymous=False)
        self.pub = rospy.Publisher("/data_acquisition/Velocity", Float64, queue_size=10)     # Publishing to the topic "Frequency"
        self.dist_sub = rospy.Subscriber("/tag_calib/bed_displacement", Float64, self.callback_Distance)
        self.pub_calibstate = rospy.Publisher('calibration_parameters', calib_msg, queue_size=10)
        self.trigger = False
        self.multipler = 1.0
        self.Publish_Velocity()
        rospy.spin()

    def callback_Distance(self,data):
        self.actual_disp = data.data
        if(self.actual_disp != 0.0):
            self.multipler = self.disp / (self.actual_disp/100)
    
    def publish_data(self):
        msg = calib_msg()
        msg.left_ls = False
        msg.right_ls = False
        msg.bed_length = 0.0
        msg.bed_position = 0.0   # Publish the user defined position in mm
        msg.pgd_calib_trigger = self.trigger
        self.pub_calibstate.publish(msg)


    def Publish_Velocity(self):
        
        tic = time.time()
        toc = 0.0
        while toc < 0.5:
            toc = time.time() - tic
            self.pub.publish(-0.01)
            time.sleep(1/self.Hz)
        self.pub.publish(0.0)

        tic = time.time()
        toc = 0.0
        while toc < 0.5:
            toc = time.time() - tic
            self.pub.publish(0.01)
            time.sleep(1/self.Hz)
        self.pub.publish(0.0)

        rospy.sleep(1)

        input("Press Enter to Continue and Mark Initial Position")
        
        self.rate = rospy.Rate(self.Hz)

        self.T = 1/self.F

        self.step_nm = int((self.T * self.Hz)/2) + 1  # Divied by 2 because we need the bed to move in one direction only
        
        #print(self.step_nm)

        self.j = 0
        
        self.displacement = 0.0
        self.disp = 0.0

        # disp = np.zeros(self.step_nm)
        # vel = np.zeros(self.step_nm)
        # t = np.array(range(self.step_nm))
        # t = t/self.Hz

        self.trigger = True
        tic = time.time()
        toc = 0.0
        while toc < 0.5:
            toc = time.time() - tic
            self.publish_data()
            time.sleep(0.1)


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

        self.trigger = False
        tic = time.time()
        toc = 0.0
        while toc < 0.5:
            toc = time.time() - tic
            self.publish_data()
            time.sleep(0.1)

        time.sleep(1)
        
        print("The Computed Displacement is: ",round(self.disp*100,2)," cms")
        # self.actual_disp = float(input("Enter the Actual Displacement in cms: "))
        print(" The Actual Displacement is: ",round(self.actual_disp,2)," cms")

        print("The Multiplier is: ",round(self.multipler,2))0
        
        if(self.multipler!=0.0):
            self.csv_update()
        else:
            print("Multipler Error")
        
        exit()
        
    def csv_update(self):
        self.file_read = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Parameters.csv')
        type(self.file_read)
        self.csvreader = csv.reader(self.file_read)
        self.rows=[]
        for row in self.csvreader:
                self.rows.append(row)
        self.file_read.close()

        for i in range(0,len(self.rows)):
            if(self.rows[i][0]=="Velocity_Multiplier"):
                self.rows[i][1] = round(self.multipler,4)

        self.file_write = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Parameters.csv','w')
        self.writer = csv.writer(self.file_write)
        for i in range(0,len(self.rows)):
            self.writer.writerow(self.rows[i])
        self.file_write.close()

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
