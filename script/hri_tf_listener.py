#!/usr/bin/env python

## --> --> --> 
## roslaunch hri_hand_control hri_hand_control.launch
## rosrun hri_hand_control hri_tf_listener.py


import rospy, time, tf
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

class HJ_hand_tf_listener():    
   def __init__(self):
      rospy.init_node('hj_tf_listener')

   def listener(self):
      little_tf_listener = tf.TransformListener()
      target_frame = '/index_MCP'
      #ref_frame = '/knuckle_little'
      #target_frame = '/knuckle_little'
      ref_frame = '/knuckle_index'

      little_tf_listener.waitForTransform(target_frame, ref_frame, rospy.Time(), rospy.Duration(4))
      #(ee_little_trans, ee_little_rot) = little_tf_listener.lookupTransform(target_frame, ref_frame, rospy.Time(0))


      (ee_little_trans, ee_little_rot) = little_tf_listener.lookupTransform(target_frame, ref_frame, rospy.Time(0))
      print "trans: ", ee_little_trans
      print "rot:   ", ee_little_rot   



          
if __name__ == '__main__':
   hj_tf = HJ_hand_tf_listener()
   
   while not rospy.is_shutdown():       
      hj_tf.listener()
      
   

   '''
   while not rospy.is_shutdown():
      hj_tf.talker()
      hj_tf.listener()        
   '''
    
        