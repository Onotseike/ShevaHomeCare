#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
global langSelect, startSTT,dataText

ttsObject = TTSClass()
sttObject = STTClass()

#Call Back Fxns
def ItemsDataCallBack(data):
    #global dataText
    dataText = ''
    numItems = data.data[0]
    print numItems

    notDoneItems = data.data[1]
    print notDoneItems

    #dataText += 'You have ' + str(numItems) + ' items on your To Do list. With ' + str(notDoneItems) + '  items not done. Here is a summary:' 


def DrugDataCallBack(data):
    #global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    drugName = data.data
    print drugName
    

def MealDataCallBack(data):
    #global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    mealName = data.data
    print mealName
    

def ExerciseDataCallBack(data):
#3global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    exerciseName = data.data
    print exerciseName
    pass

def MiscDataCallBack(data):
    #global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    miscName = data.data
    print miscName
    #dataText += '. '
    #ttstResponsettsObject.GetTTSData(dataText)
    pass

def IntroDataCallBack(data):
    global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    dataText = data.data
    print dataText
    TTSSpeak()

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
        #sttObject.TranscribeSpeechWebSocket()
        #sttObject.GetTranscribedText()
        
    pass

#Initialize ROS Node and Subscriber

def ROSSetup():
    #global dataText
    rospy.init_node('sheva_node_handle', anonymous=True)

    itemsSubscriber = rospy.Subscriber("/ItemsPublisher",Int32MultiArray,ItemsDataCallBack)
    #print 1
    drugSubscriber = rospy.Subscriber("/DrugPublisher",String,DrugDataCallBack)
    #print 2
    mealSubscriber = rospy.Subscriber("/MealPublisher",String,MealDataCallBack)
    #print 3
    exerciseSubscriber = rospy.Subscriber("/ExercisePublisher",String,ExerciseDataCallBack)
    #print 4
    miscSubscriber = rospy.Subscriber("/MiscPublisher",String,MiscDataCallBack)  

    introSubscriber = rospy.Subscriber("/IntroPublisher",String,IntroDataCallBack)  
    #print 5
    langSubscriber = rospy.Subscriber("/LangPublisher",String,LangDataCallBack)    

    sttSubscriber = rospy.Subscriber("/StartSTTPublisher",Bool,StartSTTDataCallback)  

    
    
    rospy.spin()

def TTSSpeak():
    global dataText
    #print dataText
    ttsResponse,data = ttsObject.GetTTSData(dataText)
    while ttsResponse.status != 200:
        ttsObject.ReAuthenticate()
        ttsResponse,data = ttsObject.GetTTSData(dataText)
    ttsObject.TTSSpeak(ttsResponse,data)





if __name__ == '__main__':
    
    try:
        ROSSetup()
        

    except rospy.ROSInterruptException  as exception:
        print exception.message

    