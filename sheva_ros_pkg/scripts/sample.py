#!/usr/bin/env python

import rospy
import os 
import sys

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int32MultiArray

from cv_bridge import CvBridge,  CvBridgeError
from sheva_ros_pkg.msg import kabanitems

from STTClass import STTClass
from TTSClass import TTSClass

global numItems, notDoneItems, mealName, drugName, exerciseName, miscName, miscDes
global langSelect, startSTT

ttsObject = TTSClass()
sttObject = STTClass()

#Call Back Fxns
def ItemsDataCallBack(data):
    
    numItems = data.data[0]
    print numItems

    notDoneItems = data.data[1]
    print notDoneItems

    dataText = 'You have ' + numItems + ' of To Do, with ' + notDoneItems + '  items not done. Here is a summary.' 
    ttsObject.GetTTSData(dataText)
    
    pass

def DrugDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    drugName = data.data
    print drugName
    ttsObject.GetTTSData(drugName)

    pass

def MealDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    mealName = data.data
    print mealName
    ttsObject.GetTTSData(mealName)
    pass

def ExerciseDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    exerciseName = data.data
    print exerciseName
    ttsObject.GetTTSData(exerciseName)
    pass

def MiscDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    miscName = data.data
    print miscName
    ttsObject.GetTTSData(miscName)
    pass

def LangDataCallBack(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    langSelect = data.data
    print langSelect    
    pass

def StartSTTDataCallback(data):
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    startSTT = data.data
    print startSTT
    if startSTT:
        sttObject.RecordSpeech()
        sttObject.TranscribeSpeech()
        sttObject.GetTranscribedText()
        sttObject.TranscribeSpeechWebSocket()
        sttObject.GetTranscribedText()
        
    pass

#Initialize ROS Node and Subscriber

def ROSSetup():
    
    rospy.init_node('sheva_node_handle', anonymous=True)

    itemsSubscriber = rospy.Subscriber("/ItemsPublisher",Int32MultiArray,ItemsDataCallBack)

    drugSubscriber = rospy.Subscriber("/DrugPublisher",String,DrugDataCallBack)

    mealSubscriber = rospy.Subscriber("/MealPublisher",String,MealDataCallBack)

    exerciseSubscriber = rospy.Subscriber("/ExercisePublisher",String,ExerciseDataCallBack)

    miscSubscriber = rospy.Subscriber("/MiscPublisher",String,MiscDataCallBack)    

    langSubscriber = rospy.Subscriber("/LangPublisher",String,MiscDataCallBack)    

    sttSubscriber = rospy.Subscriber("/StartSTTPublisher",String,MiscDataCallBack)  

     

    rospy.spin()

if __name__ == '__main__':
    
    try:
        ROSSetup()
       

    except rospy.ROSInterruptException  as exception:
        print exception.message