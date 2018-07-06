#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, json
import pyaudio, wave
from xml.etree import ElementTree as ET



class SpeechClass:
    #Class for all things relating to Speech Services.

    #Variables
    apiKey = "569cb77237894b4581bebd1e84de94ff"
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    AccessTokenHost = "westus.api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    AccessToken = ""

    #Constructor
    def __init__(self): 
        self.GetAccessToken(SpeechClass.AccessTokenHost,SpeechClass.path,SpeechClass.params,SpeechClass.headers)
    

    def GetAccessToken(self, accessTokenHost,  path, params, headers) :
        print "Attempting to Connect to the  Server to get Access Token"

        _connection = httplib.HTTPSConnection(accessTokenHost)
        _connection.request("POST", path, params, headers)

        _reponseResult = _connection.getresponse()
        _data = _reponseResult.read()
        _connection.close()
        SpeechClass.AccessToken = _data.decode("UTF-8")
        
        print "Status of Request : " + _reponseResult.status
        print
        print "Reason for Response : " + _reponseResult.reason
        print 
        print "Access Token obtained is : " + SpeechClass.AccessToken
        

    def GetTTSData(self, voiceXML, dataText):
        xmlTree = ET.parse('/src/voicefile.xml')
        voiceTag = xmlTree.find('voice')
        voiceTag.text = dataText

        print  ET.tostring(xmlTree)
        print

        _headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
			"Authorization": "Bearer " + SpeechClass.AccessToken, 
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
			"User-Agent": "ShevaTTS"}

        print "Connecting to Server to Synthesize the Wave"

        _connection = httplib.HTTPSConnection("westus.tts.speech.microsoft.com")
        _connection.request("POST", "/cognitiveservices/v1", ET.tostring(xmlTree),_headers)

        _responseResult = _connection.getresponse()
        _data = _responseResult.read()
        
        print "Status of Request : " + _responseResult.status
        print
        print "Reason for Response : " + _responseResult.reason
        print 

        _pyAudio = pyaudio.PyAudio()
        _stream = _pyAudio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        _stream.write(_data)
        _stream.close()
        _connection.close()
