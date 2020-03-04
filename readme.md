# HRI hand control
Hardware X journal paper: [An Open-source Anthropomorphic Robot Hand System: HRI Hand](https://www.sciencedirect.com/science/article/pii/S2468067220300092?via%3Dihub)
## Overview

This is a ROS package developed for controling and visulalizing the HRI hand.  
The packages have been tested under ROS Kinetic and Ubuntu 16.04.  

The hardware CAD files are upload in the [An Open-source Anthropomorphic Robot Hand System: HRI Hand](https://osf.io/sfpb2/)  
And the firmware files are upload in the [HRI-hand-firmware](https://github.com/MrLacquer/HRI-hand-firmware.git)

Our robot hand system was developed with a focus on the end-effector role of the collaborative robot manipulator.   
HRI hand is a research platform that can be built at a lower price (approximately $500, using only 3D printing) than commercial end-effectors.   
Moreover, it was designed as a two four-bar linkage for the under-actuated mechanism and provides pre-shaping motion similar to the human hand prior to touching an object.

The proposed robot hand imitated the human hand, the four fingers, excluding the thumb, consist of distal interphalangeal(DIP), proximal interphalangeal(PIP), metacarpophalangeal(MCP) joints.   
The thumb part consists of interphalangeal(IP), metacarpophalangeal(MCP), Carpometacarpal(CMC) joint, and operates MCP and CMC joint with two motors.   
The motor is controlled based on the control signal received by the Micro-Controller unit (MCU) via Bluetooth communication.


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

## Description

- Classification of the revolute joint and prismatic joint.

    <img width="500" src="https://user-images.githubusercontent.com/4105524/64685394-e4911200-d4c1-11e9-800a-593bde84d98b.png"  alt="classification_revoluition_prismatic_joint" title="classification_revoluition_prismatic_joint">

    <!--![classification_revoluition_prismatic_joint](https://user-images.githubusercontent.com/4105524/64685394-e4911200-d4c1-11e9-800a-593bde84d98b.png)-->

- The tf tree of the four finger

    ![tf_tree_of_the_on_finger](https://user-images.githubusercontent.com/4105524/64685465-05596780-d4c2-11e9-946e-2e31c2ed9ed9.png)

- The tf tree of the thumb part
    ![tf_tree_thumb_part](https://user-images.githubusercontent.com/4105524/64685508-186c3780-d4c2-11e9-81bf-686ff3483fe0.png)
        


## Demo

- The HRI hand with ROS Rviz package, click image to the YouTube video.

    [<img width="500" src="https://user-images.githubusercontent.com/4105524/64685367-d4793280-d4c1-11e9-9f46-b95a5d97acb8.PNG"  alt="video_capture" title="video_capture">](https://youtu.be/vD6ZCrParco)

   <!-- [![video_capture](https://user-images.githubusercontent.com/4105524/64685367-d4793280-d4c1-11e9-9f46-b95a5d97acb8.PNG)](https://youtu.be/vD6ZCrParco) -->

- The grasp performance with UR3 manipulator, click image to the YouTube video.
    
    [<img width="500" src="https://user-images.githubusercontent.com/4105524/74118413-b3e30f00-4bfe-11ea-9a6d-40371ff9da5b.PNG"  alt="grasp performance with UR3 manipulator" title="grasp performance with UR3 manipulator">](https://www.youtube.com/watch?v=c5Ry3tl9FVw)

   <!-- [![hri_hand_hold-on](https://user-images.githubusercontent.com/4105524/64670413-f235a000-d49f-11e9-8ccc-b73484fcb043.PNG)](https://youtu.be/vkenz0KlCYk)
   -->

- The pick & place test with UR3 manipulator, click image to the YouTube video.
   
    [<img width="500" src="https://user-images.githubusercontent.com/4105524/64670616-c1a23600-d4a0-11e9-8861-e7aa47693b21.jpg"  alt="ur_manipulator_test" title="ur_manipulator_test">](https://youtu.be/8BtP_0Ygy6g)
    
   <!-- [![ur_manipulator_test](https://user-images.githubusercontent.com/4105524/64670616-c1a23600-d4a0-11e9-8861-e7aa47693b21.jpg)](https://youtu.be/8BtP_0Ygy6g)
    -->


