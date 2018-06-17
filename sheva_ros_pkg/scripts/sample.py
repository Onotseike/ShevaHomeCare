#!/usr/bin/env python

import rospy
import os 
import sys

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int32MultiArray

from cv_bridge import CvBridge,  CvBridgeError
from sheva_ros_pkg.msg import kabanitems

global numItems, notDoneItems, mealName, mealDes, drugName, drugDes, exerciseName, exerciseDes, miscName, miscDes

#Call Back Fxns
def ItemsDataCallBack(data):
    
    numItems = data.data[0]
    print numItems

    notDoneItems = data.data[1]
    print notDoneItems

    pass

def DrugDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    drugName = data.data
    print drugName

    pass

def MealDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    mealName = data.data
    print mealName

    pass

def ExerciseDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    exerciseName = data.data
    print exerciseName

    pass

def MiscDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    miscName = data.data
    print miscName
    
    pass

#Initialize ROS Node and Subscriber

def ROSSetup():
    
    rospy.init_node('sheva_node_handle', anonymous=True)

    itemsPublisher = rospy.Subscriber("/ItemsPublisher",Int32MultiArray,ItemsDataCallBack)

    drugPublisher = rospy.Subscriber("/DrugPublisher",String,DrugDataCallBack)

    mealPublisher = rospy.Subscriber("/MealPublisher",String,MealDataCallBack)

    exercisePublisher = rospy.Subscriber("/ExercisePublisher",String,ExerciseDataCallBack)

    miscPublisher = rospy.Subscriber("/MiscPublisher",String,MiscDataCallBack)    

    rospy.spin()

if __name__ == '__main__':
    try:
        ROSSetup()

    except rospy.ROSInterruptException  as exception:
        print exception.message