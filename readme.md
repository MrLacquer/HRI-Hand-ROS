# HRI hand control

## Overview

This is a ROS package developed for controling and visulalizing the HRI hand.

The packages have been tested under ROS Kinetic and Ubuntu 16.04, 

**Author: [Hyeonjun Park](https://www.linkedin.com/in/hyeonjun-park-41bb59125), koreaphj91@gmail.com**

**Affiliation: [Human-Robot Interaction LAB](https://khu-hri.weebly.com), Kyung Hee Unviersity, South Korea**



## Installation
- Before do this, please backup important files.

### Dependencies

This software is built on the Robotic Operating System ([ROS](http://wiki.ros.org/ROS/Installation)).

One line install: https://cafe.naver.com/openrt/14575 
```
for Desktop

wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh
```

## How to start?

```
$ cd ~/catkin_ws/src && git clone https://github.com/MrLacuqer/HRI-Hand-ROS.git
$ cd ~/catkin_ws && catkin_make
$ rospack profile && rosstack profile

$ roslaunch hri_hand_control hri_hand_control.launch
$ rosrun hri_hand_control hri_joint_state_pub.py
```

## Video