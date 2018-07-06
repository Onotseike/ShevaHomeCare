#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, json
import pyaudio, wave, sys

from RecognizeCallback import MyRecognizeCallback

from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback

from array import array
from struct import pack

from record import record_to_file


class STTClass:

    #Variables
    speechToText = SpeechToTextV1(
        username='55bd65da-0eb1-4721-bf1c-ddb9b8632314',
        password='ntzBRUkuU7Li',
        url='https://stream.watsonplatform.net/speech-to-text/api')

    #print(json.dumps(speechToText.list_models(), indent=2))

   # print(json.dumps(speechToText.get_model('en-US_BroadbandModel'), indent=2))

    #Constructor
    def __init__(self):
        self.audiofile = 'audio.wav'
        self.speechToText = STTClass.speechToText
        self.recognizeCallback = MyRecognizeCallback()
        self.transcribedText = ''
        #self.lang_model = lang
        print "Speech to Text Object Created"

    def RecordSpeech(self):
        print "please speak a word into the microphone"
        record_to_file(join(dirname(__file__),self.audiofile))
        print "done - result written to audio.wav"

    def TranscribeSpeech(self,):
        with open(join(dirname(__file__),self.audiofile),'rb') as audio_file:
            transcribedResult = self.speechToText.recognize(audio=audio_file, content_type='audio/wav', timestamps=False, word_confidence=False)           

            #print json.dumps(transcribedResult,indent=2)
            print 
            self.transcribedText =  transcribedResult['results'][0]['alternatives'][0]['transcript']
        
        
    def TranscribeSpeechWebSocket(self):
        with open(join(dirname(__file__),self.audiofile),'rb') as audio_file:
             self.speechToText.recognize_with_websocket(audio=audio_file, recognize_callback=self.recognizeCallback)
        
        self.transcribedText = self.recognizeCallback.GetTranscribedText()

    def GetTranscribedText(self):
        print self.transcribedText
        return self.transcribedText

      

def main():
    testClass = STTClass()
    #testClass.RecordSpeech()
    testClass.TranscribeSpeech()
    testClass.GetTranscribedText()
    testClass.TranscribeSpeechWebSocket()
    testClass.GetTranscribedText()

if __name__ == '__main__':
    main()