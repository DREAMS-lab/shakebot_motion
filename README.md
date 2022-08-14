# ShakeBot Motion
## Repository which helps to setup the Shake Table Motor-Drive and Raspberry Pi to achieve low level Control.

The package consists of files which will be used to setup the Raspberry Pi to control the Shake Table Motor-Drive using ROS. The package contains two python scripts which will launch a publisher and subscriber node, which will in turn control the motor. 

## Circuit Setup and Wiring 

The circuit consists of four main components which are: 
- [Power Supply](https://bit.ly/shake_table_motor_driver)
- [Motor](https://bit.ly/shake_table_motor_driver)
- [Motor Driver](https://bit.ly/shake_table_motor_driver)
- [Raspberry Pi](https://bit.ly/Raspberry_Pi_4)

**Wiring Diagram** : ![Wiring Diagram](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Circuit%20Diagram.jpg).


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

**Raspberry Pi PIN Diagram** : ![Raspberry Pi PIN Configuration](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Raspberry%20Pi%20GPIO%20Pins.png)


**DIP Switch Configuration**

The DIP Switches on the Motor Driver allows us to change the value for Pulses per Revolution, it the number of pulses required to complete one revolution. The default value is set to 2000 to match with [Stepper Motor Torque Curve](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Torque%20Curve.pdf).

![DIP Switch Configuration](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Dip_Switch.png)

The Default Configuration is as follows:
|DIP Switch Number|Position|
|---------------|---------------|
|SW1|OFF|
|SW2|ON|
|SW3|ON|
|SW4|OFF|
|SW5|ON|
|SW6|ON|
|SW7|ON|
|SW8|ON|

**RS232 Communication Port**

There is a RS232 Communication Port present on the Motor Driver which helps us to connect the driver to the a Windows computer to use the [Debugging software](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/STEPPERONLINE_v2.0.0.exe). The manual for the software is available [here](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Software%20Manual.pdf).

**Safety Switches**

Currently we have implemented three safety switches into the circuit, which act as fail-safe mechanisms to prevent injury to users and damage to the equipment. 

- The fail-safe switches are two limit switches on either side of the bed which prevents the bed from hitting the frame. These are Normally Closes (NO) switches, so upon contact they activate the signal to ENA+ port on the motor driver there by stopping the motor and disabling it, (i.e.) the power to the motor is cut off.
- The Manual Kill Switch is also provided which will serve as the last line of safety to kill the whole circuit. In this case the switch is a Normally Closed (NC) switch and is connected in between the power supply and the motor driver. So, upon activation the circuit breaks and the supply to the motor driver is cut and the motor is disabled. 

**Please ensure that proper grouding is done to the components to reduce risk of electrical shocking**
## Parameters Setup

The system has various parameters that be modified by the user. For example the GPIO pins, the Hub Diameter and Step Angle can be changed. Since the GPIO pins can be changed, the user needs to update the same in the [Parameters.csv](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/Parameters.csv) file. Similarly the Hub Diameter may change if the user decided to use a different belt or hub, so the same had to be updated in the [Parameters.csv](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/Parameters.csv) file. Upon running the calibration file the total step for bed to translate from one end to other end will also be updated and the distance per unit step will also be updated.
## Calibration

The system has a self calibration procedure which will help the user to position bed in the desired postion. In order to carry out the calibration the user must follow the following commands in the terminal:
```
cd ~/catkin_ws/src/shakebot_motion/src
python3 Calibration.py
```
This will make the bed to move from one end to other end and calibrate the system. Thereafter it will require the user to input the desired position of the bed, the user has to enter in terms of percentage. So the bed will move that cerain percentage from the end where it is. So for example, if the bed is at the right end and the user enters 20%, then the bed will move 20% of the total length towards right side.

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
In the Second Terminal, run the following command, this will launch the [subscriber node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/Motor_Controller.py) and will be waiting for the publisher node to publish the frequency.
```
cd ~/catkin_ws/src/shakebot_motion/src
python3 Motor_Controller.py
```
In the Third Terminal, run the following command, this will launch the [publisher node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/Velocity_Publisher.py) and start publishing the frequency, so before you launch this file please take a look at the code to set the velocity and other parameters.
```
cd ~/catkin_ws/src/shakebot_motion/src 
python3 Velocity_Publisher.py
```
**Formulation for Frequecncy Calculation :**

Frequency = (Pulses per Second) * 20

Pulese Per Second = (Rotational Speed in rpm) / ((step angle/360) * 60)

Step Angle = 1.8 Degrees (Can be reffered in [Stepper Motor Data Sheet](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Data%20Sheet.pdf))

Rotational Speed (Revolutions per Minute) = Linear Velocity * 60 / (Hub Diameter / 2)

Hub Diameter = Diameter of Pulley + 2*Thickness of Belt

## Restrictions and Limitations

Even though NEMA 34 motors can attain [maximum speed of 4000 RPM](https://bit.ly/motor_max_speed), we have limited it to 1200 RPM to ensure longevity of the motor. So, if the velocity is higher than 1200 RPM, the [subscriber node](https://github.com/DREAMS-lab/shakebot_motion/blob/master/src/Motor_Controller.py) will terminate.

## Precautions to be taken before and whilst operation ##

- Keep the manual Kill-Switch at reach and away from the apparatus so that it can be activated when needed.
- Always check the wiring to all the ports are properly connected before turning on the apparatus.

## Links to Manuals and Software

[Information on Circuit Diagram and Setup Process](https://bit.ly/shake_table_control_doc)

[Motor and Motor-Driver Product Page](https://bit.ly/shake_table_motor_driver)

[Motor-Driver Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Motor-Driver%20Manual.pdf)

[Stepper Motor Data Sheet](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Data%20Sheet.pdf)

[Stepper Motor Torque Curve](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Stepper%20Motor%20Torque%20Curve.pdf)

[Power Supply Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Power%20Supply%20Manual.pdf)

[Windows Debugging Software for Motor Driver](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/STEPPERONLINE_v2.0.0.exe)

[Debugging Software Manual](https://github.com/DREAMS-lab/shakebot_motion/blob/master/assets/Software%20Manual.pdf)
