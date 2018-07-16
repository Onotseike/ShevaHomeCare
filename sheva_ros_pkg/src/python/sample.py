#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os 
import sys

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int32MultiArray

from cv_bridge import CvBridge,  CvBridgeError

from DialogManagerClass import DialogManager
from STTClass import STTClass
from TTSClass import TTSClass

global numItems, notDoneItems, mealName, drugName, exerciseName, miscName, miscDes
global langSelect, startSTT,dataText
global onLogin

global _dialogManager
_dialogManager = DialogManager("english")
#ttsObject = TTSClass()
#sttObject = STTClass()


#Call Back Fxns
def LangDataCallBack(data):
    global _dialogManager, langSelect
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    langSelect = data.data
    _dialogManager = DialogManager(langSelect)
    print langSelect
    pass

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

def MiscDataCallBack(data):
    #global dataText
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    miscName = data.data
    print miscName    

def IntroDataCallBack(data):
    global dataText, _dialogManager, onLogin
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    dataText = data.data
    print dataText
    if _dialogManager == None:
            _dialogManager = DialogManager(langSelect)
    #if onLogin == True:
        #_dialogManager.SetCurrentSate("LoginState")
    intentName, msgArray = _dialogManager.IntroGreeting("Paula", dataText)
    if intentName == "CRUDTodolist" or intentName == "QueryTodoList":
        queryArray = Int32MultiArray(data=msgArray)
        #todoListQueryPublisher.publish(queryArray)
        TodoListPublish(queryArray)
    elif intentName == "LanguageChange":
        language = msgArray[0] #_dialogManager.GetCurrentLanguage()
        languangeChangePublisher.publish(language)

    else:
        _dialogManager.SetCurrentSate("DefaultState")
    #Execute Action based on intentName
    #_dialogManager.TTSSpeakLanguage(dataText)
    #TTSSpeak()

def StartSTTDataCallback(data):
    global _dialogManager, langSelect
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    startSTT = data.data
    print startSTT
    if startSTT:
        if _dialogManager == None:
            _dialogManager = DialogManager(langSelect)

        luisFeed = _dialogManager.STTLanguage()
        if luisFeed == "":
            _dialogManager.TTSSpeakLanguage("My Apologies, I could not understand what was said. Try again.")
            intentName, msgArray = "None", []
        else:
            intentName, entityParams = _dialogManager.LUISUnderstand(_dialogManager.TransLateText("english",luisFeed))
            intentName, msgArray = _dialogManager.StateSwitcher(intentName, entityParams)
        
        #Switching statement based on intent
        if intentName == "CRUDTodolist" or intentName == "QueryTodoList":
            queryArray = Int32MultiArray(data=msgArray)
            #todoListQueryPublisher.publish(queryArray)
            TodoListPublish(queryArray)
        elif intentName == "LanguageChange":
            language = msgArray[0] #_dialogManager.GetCurrentLanguage()
            languangeChangePublisher.publish(language)

        else:
            pass
        #sttObject.RecordSpeech()
        #sttObject.TranscribeSpeech()
        #sttObject.GetTranscribedText()
        #sttObject.TranscribeSpeechWebSocket()
        #sttObject.GetTranscribedText()
        
def QueryResultCallBack(data):
    global dataText, _dialogManager, onLogin
    rospy.loginfo(rospy.get_caller_id() + "Echoed %s", data.data)
    dataText = data.data
    print dataText
    _dialogManager.TTSSpeakLanguage(dataText)
    
    
  

#Initialize ROS Node Publishers and Subscribers

def ROSSetup():
    global onLogin,todoListQueryPublisher,languangeChangePublisher
    rospy.init_node('sheva_node_handle', anonymous=True)

    todoListQueryPublisher = rospy.Publisher(
        '/todoListQueryPublisher', Int32MultiArray, queue_size=10)
    languangeChangePublisher = rospy.Publisher("/LanguageChangePublisher", String, queue_size=10)

    langSubscriber = rospy.Subscriber("/LangPublisher", String, LangDataCallBack)

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
    
    sttSubscriber = rospy.Subscriber("/StartSTTPublisher", Bool, StartSTTDataCallback)
    rospy.Subscriber("/QueryResultPublisher", String, QueryResultCallBack)
    
    onLogin = True

    
    
    rospy.spin()

def TTSSpeak():
    global dataText
    #print dataText
    ttsResponse,data = ttsObject.GetTTSData(dataText)
    while ttsResponse.status != 200:
        ttsObject.ReAuthenticate()
        ttsResponse,data = ttsObject.GetTTSData(dataText)
    ttsObject.TTSSpeak(ttsResponse,data)

def TodoListPublish(data):
    global todoListQueryPublisher
    todoListQueryPublisher.publish(data)



if __name__ == '__main__':
    
    try:
        ROSSetup()
        

    except rospy.ROSInterruptException  as exception:
        print exception.message

    
