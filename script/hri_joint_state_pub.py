#!/usr/bin/env python
#-*- coding:utf-8 -*-

## --> --> --> 
## roslaunch hri_hand_control hri_hand_control.launch
## rosrun hri_hand_control hri_joint_state_pub.py


import rospy, time, tf
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

import serial

class STM_serial():
    def __init__(self):
        self.rx_data = 0
        self.tx_data = 0
        self.PORT = '/dev/ttyUSB0'
        self.BaudRate = 115200

        #print 'serial', serial.__version__
        self.ser = serial.Serial(self.PORT, self.BaudRate)

        self.ii = 0 
        #print self.ser

    def send_signal(self, motor_id, motor_val):
        #A = [0x01, 0x02, 0x03, 0x04, 0x05]
        
        self.ser.write(bytes(bytearray([motor_id])))
        self.ser.write(bytes(bytearray([motor_val])))        

        print "serial class: ", motor_id, motor_val
        '''
        if self.ser.readable():
            RxValue = self.ser.readline()
            print "Rx: ", RxValue
        '''


class HJ_hand_tf():    
    """
    xxx_talker(): finger bending - stretching in the Rviz \n
    ex) \n
    while not rospy.is_shutdown():
        hj_tf.little_talke()
        hj_tf.index_talker()
        hj_tf.middle_talker()
        hj_tf.ring_talker()
        hj_tf.thumb_joint_talker()
        hj_tf.thumb_talker()
       
    """
    def __init__(self):
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        rospy.init_node('hj_joint_state_publisher')
        self.rate = rospy.Rate(30) # 60hz
        self.hello_str = JointState()
        self.hello_str.header = Header()
        self.hello_str.header.stamp = rospy.Time.now()
        #hello_str.name = ['index_MCP', 'index_PIP']
        self.hello_str.name = [
            'thumb_jo_joint', 
            'thumb_MCP_joint', 
            'thumb_DIP_joint',
            'pris_thumb_jo_joint',
            'pris_thumb_DIP_joint',
            'index_MCP_joint',
            'index_PIP_joint', 
            'index_DIP_joint', 
            'middle_MCP_joint', 
            'middle_PIP_joint',
            'middle_DIP_joint', 
            'ring_MCP_joint', 
            'ring_PIP_joint', 
            'ring_DIP_joint', 
            'little_MCP_joint',  
            'little_PIP_joint', 
            'little_DIP_joint', 
            'pris_index_joint', 
            'pris_middle_joint', 
            'pris_ring_joint',
            'pris_little_joint']
        self.hello_str.position = [0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.hello_str.velocity = []
        self.hello_str.effort = []

        self.pri_index  = 0  
        self.pri_middle  = 0  
        self.pri_ring  = 0  
        self.pri_little  = 0  
        self.pri_thumb  = 0  
        self.pri_thumb_j  = 0  

        self.index_MCP = 0
        self.index_PIP = 0
        self.index_DIP = 0
        self.middle_MCP = 0
        self.middle_PIP = 0
        self.middle_DIP = 0
        self.ring_MCP = 0
        self.ring_PIP = 0
        self.ring_DIP = 0        
        self.little_MCP = 0
        self.little_PIP = 0
        self.little_DIP = 0
        self.thumb_MCP = 0        
        self.thumb_DIP = 0
        self.thumb_joint = 0

        self.rad_max = [1.22173, 1.0472, 0.872265] #70degree, 60 degree, 50 degree
        
        self.in_rad_goal = [0.0, 0.0, 0.0]
        self.mi_rad_goal = [0.0, 0.0, 0.0]
        self.ri_rad_goal = [0.0, 0.0, 0.0]
        self.li_rad_goal =[0.0, 0.0, 0.0]
        self.th_rad_goal = [0.0, 0.0, 0.0]
        self.thj_rad_goal = [0.0, 0.0, 0.0]

        #self.ee_little_trans
        #self.ee_little_rot

        self.count = 0

        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)
        #self.little_tf_listener = tf.TransformListener()

        self.in_bend_flag = 0   #index finger
        self.mi_bend_flag = 0   #middle finger
        self.ri_bend_flag = 0   #ring finger
        self.li_bend_flag = 0   #little finger
        self.th_bend_flag = 0   #thumb finger
        self.thj_bend_flag = 0  #thumb joint finger

    def all_finger_action(self, pris_val):
        """
        all finger aciton : open-0.0, close-0.012
        """
        self.in_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.in_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.in_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[17] = pris_val   #pris_index
        self.hello_str.position[5] = self.in_rad_goal[0]  #index_MCP
        self.hello_str.position[6] = self.in_rad_goal[1]  #index_PIP
        self.hello_str.position[7] = self.in_rad_goal[2]  #index_DIP    

        self.mi_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.mi_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.mi_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[18] = pris_val   #pris_middle
        self.hello_str.position[8] = self.mi_rad_goal[0]  #middle_MCP
        self.hello_str.position[9] = self.mi_rad_goal[1]  #middle_PIP
        self.hello_str.position[10] = self.mi_rad_goal[2]  #middle_DIP    

        self.ri_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.ri_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.ri_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[19] = pris_val   #pris_ring
        self.hello_str.position[11] = self.ri_rad_goal[0]  #ring_MCP
        self.hello_str.position[12] = self.ri_rad_goal[1]  #ring_PIP
        self.hello_str.position[13] = self.ri_rad_goal[2]  #ring_DIP

        self.li_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.li_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.li_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[20] = pris_val    #pris_little
        self.hello_str.position[14] = self.li_rad_goal[0]  #little_MCP
        self.hello_str.position[15] = self.li_rad_goal[1]  #little_PIP
        self.hello_str.position[16] = self.li_rad_goal[2]  #little_DIP     

        self.th_rad_goal[0] = 1000 * pris_val * (self.rad_max[1]/12)
        self.th_rad_goal[1] = 1000 * pris_val * (0.523599/12)  #30 degree    

        self.hello_str.position[4] = pris_val   #pris_ring
        self.hello_str.position[1] = self.th_rad_goal[0]  #ring_MCP        
        self.hello_str.position[2] = self.th_rad_goal[1]  #ring_DIP  

        self.thj_rad_goal[0] = 1000 * pris_val  * (self.rad_max[2]/12)        

        self.hello_str.position[3] = pris_val    #pris_thumb_j
        self.hello_str.position[0] = self.thj_rad_goal[0]  #thumb_joint                      
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)      

        self.hj_finger_control(0x01, pris_val)
        self.hj_finger_control(0x02, pris_val)
        self.hj_finger_control(0x03, pris_val)
        self.hj_finger_control(0x04, pris_val)
        self.hj_finger_control(0x05, pris_val)
        self.hj_finger_control(0x06, pris_val)
  
    def index_talker(self):
        if self.in_bend_flag == 0:
            self.pri_index = self.pri_index + 0.001
            if self.pri_index > 0.012:
                self.in_bend_flag = 1

        elif self.in_bend_flag == 1:
            self.pri_index = self.pri_index - 0.001
            if self.pri_index < 0.0:
                self.in_bend_flag = 0

        print "index_talker pri_index: ", self.pri_index

        self.in_rad_goal[0] = 1000*self.pri_index *(self.rad_max[0]/12)
        self.in_rad_goal[1] = 1000*self.pri_index *(self.rad_max[1]/12)
        self.in_rad_goal[2] = 1000*self.pri_index *(self.rad_max[2]/12)

        self.hello_str.position[17] = self.pri_index   #pris_index
        self.hello_str.position[5] = self.in_rad_goal[0]  #index_MCP
        self.hello_str.position[6] = self.in_rad_goal[1]  #index_PIP
        self.hello_str.position[7] = self.in_rad_goal[2]  #index_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()        

    def middle_talker(self):
        if self.mi_bend_flag == 0:
            self.pri_middle = self.pri_middle + 0.0001
            if self.pri_middle > 0.012:
                self.mi_bend_flag = 1

        elif self.mi_bend_flag == 1:
            self.pri_middle = self.pri_middle - 0.0001
            if self.pri_middle < 0.0:
                self.mi_bend_flag = 0

        self.mi_rad_goal[0] = 1000*self.pri_middle *(self.rad_max[0]/12)
        self.mi_rad_goal[1] = 1000*self.pri_middle *(self.rad_max[1]/12)
        self.mi_rad_goal[2] = 1000*self.pri_middle *(self.rad_max[2]/12)

        self.hello_str.position[18] = self.pri_middle   #pris_middle
        self.hello_str.position[8] = self.mi_rad_goal[0]  #middle_MCP
        self.hello_str.position[9] = self.mi_rad_goal[1]  #middle_PIP
        self.hello_str.position[10] = self.mi_rad_goal[2]  #middle_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()        

    def ring_talker(self):
        if self.ri_bend_flag == 0:
            self.pri_ring = self.pri_ring + 0.0001
            if self.pri_ring > 0.012:
                self.ri_bend_flag = 1

        elif self.ri_bend_flag == 1:
            self.pri_ring = self.pri_ring - 0.0001
            if self.pri_ring < 0.0:
                self.ri_bend_flag = 0

        self.ri_rad_goal[0] = 1000*self.pri_ring *(self.rad_max[0]/12)
        self.ri_rad_goal[1] = 1000*self.pri_ring *(self.rad_max[1]/12)
        self.ri_rad_goal[2] = 1000*self.pri_ring *(self.rad_max[2]/12)

        self.hello_str.position[19] = self.pri_ring   #pris_ring
        self.hello_str.position[11] = self.ri_rad_goal[0]  #ring_MCP
        self.hello_str.position[12] = self.ri_rad_goal[1]  #ring_PIP
        self.hello_str.position[13] = self.ri_rad_goal[2]  #ring_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()        

    def little_talker(self): 
        if self.li_bend_flag == 0:
            self.pri_little = self.pri_little + 0.0001
            if self.pri_little > 0.012:
                self.li_bend_flag = 1

        elif self.li_bend_flag == 1:
            self.pri_little = self.pri_little - 0.0001
            if self.pri_little < 0.0:
                self.li_bend_flag = 0

        #print "flag, pri_little: ", self.bend_flag, self.pri_little

        self.li_rad_goal[0] = 1000*self.pri_little *(self.rad_max[0]/12)
        self.li_rad_goal[1] = 1000*self.pri_little *(self.rad_max[1]/12)
        self.li_rad_goal[2] = 1000*self.pri_little *(self.rad_max[2]/12)

        self.hello_str.position[20] = self.pri_little   #pris_little
        self.hello_str.position[14] = self.li_rad_goal[0]  #little_MCP
        self.hello_str.position[15] = self.li_rad_goal[1]  #little_PIP
        self.hello_str.position[16] = self.li_rad_goal[2]  #little_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()

        #print "now pri_little: ", pri_little

    def thumb_talker(self):
        if self.th_bend_flag == 0:
            self.pri_thumb = self.pri_thumb + 0.0001
            if self.pri_thumb > 0.008:
                self.th_bend_flag = 1

        elif self.th_bend_flag == 1:
            self.pri_thumb = self.pri_thumb - 0.0001
            if self.pri_thumb < 0.0:
                self.th_bend_flag = 0

        print "pri_thumb, th_bend_flag", self.pri_thumb, self.th_bend_flag

        self.th_rad_goal[0] = 1000*self.pri_thumb * (self.rad_max[0]/12)
        self.th_rad_goal[1] = 1000*self.pri_thumb * (0.523599/12)  #30 degree 

        self.hello_str.position[4] = self.pri_thumb   #pris_ring
        self.hello_str.position[1] = self.th_rad_goal[0]  #ring_MCP        
        self.hello_str.position[2] = self.th_rad_goal[1]  #ring_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()  

    def thumb_joint_talker(self):
        if self.thj_bend_flag == 0:
            self.pri_thumb_j = self.pri_thumb_j + 0.0001
            if self.pri_thumb_j > 0.012:
                self.thj_bend_flag = 1

        elif self.thj_bend_flag == 1:
            self.pri_thumb_j = self.pri_thumb_j - 0.0001
            if self.pri_thumb_j < 0.0:
                self.thj_bend_flag = 0

        self.thj_rad_goal[0] = 1000*self.pri_thumb_j *(self.rad_max[2]/12)        

        self.hello_str.position[3] = self.pri_thumb_j   #pris_thumb_j
        self.hello_str.position[0] = self.thj_rad_goal[0]  #thumb_joint                      
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

        #time.sleep(0.001)
        self.rate.sleep()  

    def index_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012. in Rviz
        """
        self.in_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.in_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.in_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[17] = pris_val   #pris_index
        self.hello_str.position[5] = self.in_rad_goal[0]  #index_MCP
        self.hello_str.position[6] = self.in_rad_goal[1]  #index_PIP
        self.hello_str.position[7] = self.in_rad_goal[2]  #index_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

    def middle_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012
        """
        self.mi_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.mi_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.mi_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[18] = pris_val   #pris_middle
        self.hello_str.position[8] = self.mi_rad_goal[0]  #middle_MCP
        self.hello_str.position[9] = self.mi_rad_goal[1]  #middle_PIP
        self.hello_str.position[10] = self.mi_rad_goal[2]  #middle_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

    def ring_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012
        """
        self.ri_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.ri_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.ri_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[19] = pris_val   #pris_ring
        self.hello_str.position[11] = self.ri_rad_goal[0]  #ring_MCP
        self.hello_str.position[12] = self.ri_rad_goal[1]  #ring_PIP
        self.hello_str.position[13] = self.ri_rad_goal[2]  #ring_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

    def little_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012
        """
        self.li_rad_goal[0] = 1000 * pris_val * (self.rad_max[0]/12)
        self.li_rad_goal[1] = 1000 * pris_val * (self.rad_max[1]/12)
        self.li_rad_goal[2] = 1000 * pris_val * (self.rad_max[2]/12)

        self.hello_str.position[20] = pris_val    #pris_little
        self.hello_str.position[14] = self.li_rad_goal[0]  #little_MCP
        self.hello_str.position[15] = self.li_rad_goal[1]  #little_PIP
        self.hello_str.position[16] = self.li_rad_goal[2]  #little_DIP    

        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)         

    def thumb_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012
        """
        self.th_rad_goal[0] = 1000 * pris_val * (self.rad_max[1]/12)
        self.th_rad_goal[1] = 1000 * pris_val * (0.610865/12)  #30 degree      

        self.hello_str.position[4] = pris_val   #pris_ring
        self.hello_str.position[1] = self.th_rad_goal[0]  #ring_MCP        
        self.hello_str.position[2] = self.th_rad_goal[1]  #ring_DIP              
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

    def thumb_joint_control(self, pris_val):
        """
        pris_val: mm unit. ex) 12mm --> 0.012
        """
        self.thj_rad_goal[0] = 1000 * pris_val  * (self.rad_max[2]/12)        

        self.hello_str.position[3] = pris_val    #pris_thumb_j
        self.hello_str.position[0] = self.thj_rad_goal[0]  #thumb_joint                      
                
        self.hello_str.header.stamp = rospy.Time.now()
        self.pub.publish(self.hello_str)

    def index_motor_talker(self):
        """
        index talker의 기능을 실제 로봇 손에 적용 가능하도록 하는 구문
        """
        self.index_talker()

        #print "pri index: ", self.pri_index
        send_pris_val = self.pri_index * 1000
        send_pris_val = int(send_pris_val)
        print "send pris: ", send_pris_val
        
        if send_pris_val < 0:
            pass
        else:                        
            stmser.send_signal(stm_index_id, send_pris_val)
            #stmser.send_signal(ssss, 0x01)
            #ssss = 0x01 + 1

    def middle_motor_talker(self):
        """
        middle talker의 기능을 실제 로봇 손에 적용 가능하도록 하는 구문
        """
        self.middle_talker()

        #print "pri index: ", self.pri_index
        send_pris_val = self.pri_middle * 1000
        send_pris_val = int(send_pris_val)
        print "send pris: ", send_pris_val
        
        if send_pris_val < 0:
            pass
        else:                        
            stmser.send_signal(stm_index_id, send_pris_val)
            #stmser.send_signal(ssss, 0x01)
            #ssss = 0x01 + 1

    def ring_motor_talker(self):
        """
        ring talker의 기능을 실제 로봇 손에 적용 가능하도록 하는 구문
        """
        self.ring_talker()

        #print "pri index: ", self.pri_index
        send_pris_val = self.pri_ring * 1000
        send_pris_val = int(send_pris_val)
        print "send pris: ", send_pris_val
        
        if send_pris_val < 0:
            pass
        else:                        
            stmser.send_signal(stm_index_id, send_pris_val)
            #stmser.send_signal(ssss, 0x01)
            #ssss = 0x01 + 1            

    def little_motor_talker(self):
        """
        little talker의 기능을 실제 로봇 손에 적용 가능하도록 하는 구문
        """
        self.little_talker()

        #print "pri index: ", self.pri_index
        send_pris_val = self.pri_little * 1000
        send_pris_val = int(send_pris_val)
        print "send pris: ", send_pris_val
        
        if send_pris_val < 0:
            pass
        else:                        
            stmser.send_signal(stm_index_id, send_pris_val)
            #stmser.send_signal(ssss, 0x01)
            #ssss = 0x01 + 1            


    def hj_finger_control(self, my_motor_id, my_pris_val):
        print "pri index: ", my_pris_val
        stm_pris_val = my_pris_val * 1000      #converting unit [m] to [mm]
        stm_pris_val = int(stm_pris_val)    #converting to integer
        print "send pris: ", stm_pris_val

        if stm_pris_val < 0:
            pass
        else:                        
            stmser.send_signal(my_motor_id, stm_pris_val)

    def hj_finger_mode01(self):
        """
        test... do not use... using in main
        """
        while not rospy.is_shutdown():  
            main_bend_flag = 0 
            hj_tf.thumb_joint_control(thumb_joint_pris_val)
            hj_tf.hj_finger_control(stm_thumb_joint_id, thumb_joint_pris_val)
            #time.sleep(1.0)

            if main_bend_flag == 0:
                index_pris_val = index_pris_val + 0.001
                if index_pris_val > 0.012:
                    main_bend_flag = 1

            elif main_bend_flag == 1:
                index_pris_val = index_pris_val - 0.001
                if index_pris_val < 0.0:
                    main_bend_flag = 0

            hj_tf.index_control(index_pris_val)
            hj_tf.hj_finger_control(stm_index_id, index_pris_val)

            hj_tf.middle_control(index_pris_val)
            hj_tf.hj_finger_control(stm_middle_id, index_pris_val)

            hj_tf.ring_control(index_pris_val)
            hj_tf.hj_finger_control(stm_ring_id, index_pris_val)

            hj_tf.little_control(index_pris_val)
            hj_tf.hj_finger_control(stm_little_id, index_pris_val)        

            hj_tf.rate.sleep()



if __name__ == '__main__':
    hj_tf = HJ_hand_tf()
    stmser = STM_serial()

    print ">> if you ready, press the Enter"
    raw_input()
    stm_index_id = 0x01
    stm_middle_id = 0x02
    stm_ring_id = 0x03
    stm_little_id = 0x04
    stm_thumb_id = 0x05
    stm_thumb_joint_id = 0x06

    index_pris_val = 0.0
    middle_pris_val = 0.012
    ring_pris_val = 0.012
    little_pris_val = 0.012
    thumb_pris_val = 0.012
    thumb_joint_pris_val = 0.012

    #main_bend_flag = 0
    
    
    hj_tf.index_control(0.012)
    hj_tf.hj_finger_control(stm_index_id, 0.012)
    time.sleep(0.5)
    hj_tf.index_control(0.0)
    hj_tf.hj_finger_control(stm_index_id, 0.0)
    time.sleep(0.5)

    hj_tf.middle_control(0.012)
    hj_tf.hj_finger_control(stm_middle_id, 0.012)
    time.sleep(0.5)
    hj_tf.middle_control(0.0)
    hj_tf.hj_finger_control(stm_middle_id, 0.0)
    time.sleep(0.5)

    hj_tf.ring_control(0.012)
    hj_tf.hj_finger_control(stm_ring_id, 0.012)
    time.sleep(0.5)
    hj_tf.ring_control(0.0)
    hj_tf.hj_finger_control(stm_ring_id, 0.0)
    time.sleep(0.5)

    hj_tf.little_control(0.012)
    hj_tf.hj_finger_control(stm_little_id, 0.012)
    time.sleep(0.5)
    hj_tf.little_control(0.0)
    hj_tf.hj_finger_control(stm_little_id, 0.0)
    time.sleep(0.5)

    hj_tf.thumb_joint_control(0.012)
    hj_tf.hj_finger_control(stm_thumb_joint_id, 0.012)
    time.sleep(0.5)
    hj_tf.thumb_control(0.012)
    hj_tf.hj_finger_control(stm_thumb_id, 0.012)
    time.sleep(0.5)

    hj_tf.thumb_control(0.0)
    hj_tf.hj_finger_control(stm_thumb_id, 0.0)
    time.sleep(0.5)
    hj_tf.thumb_joint_control(0.0)
    hj_tf.hj_finger_control(stm_thumb_joint_id, 0.0)
    time.sleep(0.5)

        
