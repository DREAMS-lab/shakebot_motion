#!/usr/bin/env python3

import rospy
from Trajectory import F_A_Publisher
from Trajectory import Velocity_Publisher
import time
from datetime import datetime
import csv
import actionlib
from shakebot_perception.msg import recorder_automationAction, recorder_automationGoal
import RPi.GPIO as GPIO
import os

class UI: 
    def __init__(self):
        
        os.system("clear")
        GPIO.setwarnings(False)
        #Getting Input from the User
        
        print("SHAKE BOT")
        self.input()


    def rock_positioned(self):                      #To check if user had placed rock on bed
        print("Please postion Rock on the Bed")
        print("If position is correct, press any key to continue")
        input()

    def rockstatus(self):                           #To check if rock is toppled or not and record it in a CSV file
        print("Is the rock toppled?(Y/N):")
        self.rock_flag = input()

        self.file = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Experiment_Data.csv')
        type(self.file)
        self.csvreader = csv.reader(self.file)
        self.rows=[]
        for row in self.csvreader:
                self.rows.append(row)
        self.file.close()

        
        self.rows.append([datetime.now(),self.PGV_2_PGA,self.PGA / 9.80665,self.rock_flag])

        self.file = open('/home/'+os.getlogin()+'/catkin_ws/src/shakebot_motion/src/Experiment_Data.csv','w')
        self.writer = csv.writer(self.file)
        for i in range(0,len(self.rows)):
            self.writer.writerow(self.rows[i])
        self.file.close()

    def camera_call_server(self, state):
        client = actionlib.SimpleActionClient("/data_acquisition/shakebot_recorder_as", recorder_automationAction)
        #print("waiting server start")
        client.wait_for_server()
        #print("waiting serverend")
        goal = recorder_automationGoal()
        goal.recorder_state = state
        client.send_goal(goal)
        #print("goal_sent")
        client.wait_for_result()
        result=client.get_result()
        #print(result)
        return result
        

    def input(self):                                #To get PGV and PGA values and calls the Velocity_Publisher() to calculate trajectory and publish velocity
        
        os.system("clear")
        print("SHAKE BOT")
        
        self.rock_positioned()
        time.sleep(1)
        
        os.system("clear")
        print("SHAKE BOT")
        
        self.recorder_state_start = False
        self.recorder_state_end = False
        
        print("Enter Peak Ground Velocity / Peak Ground Acceleration Ratio:")
        self.PGV_2_PGA = float(input())
        print("Enter Peak Ground Acceleration(Gs):")
        self.PGA = float(input())

        self.PGA = self.PGA * 9.80665   # Converting to m/s^2
        
        print("Initiating Rock Shaking")
        time.sleep(1)
        
        self.F_A = F_A_Publisher(self.PGV_2_PGA,self.PGA)
        
        while not self.recorder_state_start:
            #print("inside camera call while")
            self.recorder_state_start=self.camera_call_server(True)
            #print(self.recorder_state_start)
        
        self.F, self.A = self.F_A.F_A_Compute()
        
        # time.sleep(1)
        # rospy.loginfo("Camera Triggered")
        
        self.Velocity_Publisher = Velocity_Publisher(self.F,self.A)

        while not self.recorder_state_end:
            self.recorder_state_end=self.camera_call_server(False)
            # print(self.recorder_state_end)
        # rospy.loginfo("Camera Stopped")
        self.rockstatus()

        print("Do you want to continue?(Y/N):")
        self.continue_flag = input()
        if self.continue_flag == "Y":
            self.input()
        else:
            print("Exiting")
            rospy.signal_shutdown("Stopping")
            exit()

if __name__ == '__main__':
        
        User_Interface = UI()
        GPIO.cleanup()
