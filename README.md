# ShakeBot Motion
## Repository which helps to setup the Shake Table Motor-Drive and Raspberry Pi to achieve low level Control.

The package consists of files which will be used to setup the Raspberry Pi to control the Shake Table Motor-Drive using ROS. The package contains two python scripts which will launch a publisher and subscriber node, which will in turn control the motor. 

## Circuit Setup and Wiring 

The circuit consists of four main components which are: 
- [Power Supply](https://bit.ly/shake_table_motor_driver)
- [Motor](https://bit.ly/shake_table_motor_driver)
- [Motor Driver](https://bit.ly/shake_table_motor_driver)
- [Raspberry Pi](https://bit.ly/Raspberry_Pi_4)

The wiring diagram is as follows : [Wiring Diagram](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Circuit%20Diagram.jpg).


**Raspberry Pi PINS Configuration**

| GPIO PIN Number  | BOARD PIN Number | Description |
| --------------- | --------------- | --------------- |
| 18 | 12 | PUL+ PIN in Motor Driver |
| GND | 14 | PUL- PIN in Motor Driver |
| 20 | 38 | DIR+ PIN in Motor Driver |
| GND | 39 | DIR- PIN in Motor Driver |
| 3V | 1 | Supply to both Primary Limit Switchs |
| 17 | 11 | Primary Left Limit Switch |
| 5 | 29 | Primary Right Limit Switch |


**DIP Switch Configuration**

The DIP Switches on the Motor Driver allows us to change the value for Pulses per Revolution, it the number of pulses required to complete one revolution. The default value is set to 2000 to match with [Stepper Motor Torque Curve](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Torque%20Curve.pdf). If you intend to change it, please change the same in the [Publisher Node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/motor_test_ros_pub.py) in line #22 also.

**Please ensure that proper grouding is done to the components to reduce risk of electrical shocking**

## ROS Package Setup and Code Brief

**Please continue only if you had installed ROS and had setup the ROS environment, else please install and setup the same**

Requirements: [Ubuntu 20.04 LTS](https://bit.ly/Ubuntu_Install), [ROS Noetic](https://bit.ly/ROS_Install), [Python3](https://bit.ly/Python3_Install)

Please follow the below steps to setup the ROS package. 

```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

git clone https://github.com/DREAMS-lab/shakebot_motion.git
cd ~/catkin_ws/
catkin_make or catkin build
```
This will set up the workspace and will allow you to run the python scripts to launch the nodes. 
Please follow the next steps to launch the Publisher and Subscriber nodes. Please open 3 seperate terminals.

In the First Terminal, run the following command: 
```
roscore
```
In the Second Terminal, run the following command, this will launch the [subscriber node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/motor_test_ros_sub.py) and will be waiting for the publisher node to publish the frequency.
```
cd ~/catkin_ws/src/shakebot_motion/src
python3 motor_test_ros_sub.py
```
In the Third Terminal, run the following command, this will launch the [publisher node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/motor_test_ros_pub.py) and start publishing the frequency, so before you launch this file please take a look at the code to set the velocity and other parameters.
```
cd ~/catkin_ws/src/shakebot_motion/src 
python3 motor_test_ros_pub.py
```
The Formulation for the frequency calculation can be referred [here](https://bit.ly/shake_table_control_doc) in Page 4 Section 6.

## Restrictions and Limitations

Even though NEMA 34 motors can attain [maximum speed of 4000 RPM](https://bit.ly/motor_max_speed), we have limited it to 1200 RPM to ensure longevity of the motor. So, if the velocity is higher than 1200 RPM, the [publisher node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/motor_test_ros_pub.py) will terminate.

## Links to Manuals and Software

[Information on Circuit Diagram and Setup Process](https://bit.ly/shake_table_control_doc)

[Motor and Motor-Driver Product Page](https://bit.ly/shake_table_motor_driver)

[Motor-Driver Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Motor-Driver%20Manual.pdf)

[Stepper Motor Data Sheet](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Data%20Sheet.pdf)

[Stepper Motor Torque Curve](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Torque%20Curve.pdf)

[Power Supply Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Power%20Supply%20Manual.pdf)

[Windows Debugging Software for Motor Driver](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/STEPPERONLINE_v2.0.0.exe)

[Debugging Software Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Software%20Manual.pdf)
