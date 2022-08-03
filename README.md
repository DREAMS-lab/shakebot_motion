# ShakeBot Motion Repo
## Repository which helps to setup the Shake Table Motor-Drive and Raspberry Pi to achieve low level Control.

The package consists of files which will be used to setup the Raspberry Pi to control the Shake Table Motor-Drive using ROS. The package contains two python scripts which will launch a publisher and subscriber node, which will in turn control the motor. 

## Circuit Setup and Wiring 

The circuit consists of four main components which are: 
- Power Supply
- Motor
- Motor Driver 
- Raspberry Pi

The wiring diagram can be referred in the following link in Page 1 : https://bit.ly/shake_table_control_doc
It also consists of a test setup which shows actual photos from the prototype

###### Please ensure that proper grouding is done to the components to reduce risk of electrical shocking. 

## ROS Package Setup and Code Brief

Please follow the below steps to setup the ROS package. 

```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

git clone https://github.com/DREAMS-lab/shakebot_motion.git
cd ~/catkin_ws/
catkin_make or catkin build
```
This will set up the workspace and will allow you to run the python scripts to launch the nodes. 
Please follow the next steps to launch the Publisher and Subscriber nodes. 

```
cd ~/catkin_ws/src/shakebot_motion/src

```

## Links to Manuals and Software

Please Refer the Document for more Information on Circuit Diagram and Setup Process : https://bit.ly/shake_table_control_doc

Website Link to Motor and Motor-Driver : https://bit.ly/shake_table_motor_driver

Motor-Driver Manual : https://bit.ly/shake_table_motor_driver_manual

Stepper Motor Data Sheet : https://bit.ly/shake_table_stepper_data_sheet

Stepper Motor Torque Curve : https://bit.ly/shake_table_torque_curve

Power Supply Manual : https://bit.ly/shake_table_power_supply_manual

Windows Debugging Software : https://bit.ly/shake_table_windows_debug_software

Debugging Software Manual : https://bit.ly/shake_table_debugging_software_manual
