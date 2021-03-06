import httplib, urllib, json, string as strg
import pyaudio, wave
from xml.etree import ElementTree as ET
from os.path import join, dirname
from TranslatorClass import TranslatorClass



class TTSClass:
    #Class for all things relating to Speech Services.

    #Variables
    _languageVoices = {
        "english" : ["Microsoft Server Speech Text to Speech Voice (en-US, Jessa24KUS)", "en-us", "Female"],
        "spanish" : ["Microsoft Server Speech Text to Speech Voice (es-ES, HelenaRUS)", "es-es", "Female"],
        "italian" : ["Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)", "it-it", "Male"]
        }
    
    apiKey = "99bba026d3864a7b8df2290bb7f79fbf"
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    AccessTokenHost = "westus.api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    AccessToken = ""
    _connection = httplib.HTTPSConnection("westus.tts.speech.microsoft.com")
    #Constructor
    def __init__(self): 

        self.GetAccessToken(TTSClass.AccessTokenHost,TTSClass.path,TTSClass.params,TTSClass.headers)
    

    def GetAccessToken(self, accessTokenHost,  path, params, headers) :
        print "Attempting to Connect to the  Server to get Access Token"

        _connection = httplib.HTTPSConnection(accessTokenHost)
        _connection.request("POST", path, params, headers)

        _reponseResult = _connection.getresponse()
        _data = _reponseResult.read()
        _connection.close()
        TTSClass.AccessToken = _data.decode("UTF-8")
        
        print "Status of Request : " +str( _reponseResult.status)
        print
        print "Reason for Response : " + _reponseResult.reason
        print 
        #print "Access Token obtained is : " + TTSClass.AccessToken
      
    def ReAuthenticate(self):
        self.GetAccessToken(TTSClass.AccessTokenHost,TTSClass.path,TTSClass.params,TTSClass.headers)
    

    def GetTTSData(self, dataText):  

        body = ET.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        body.set('xmlns', 'http://www.w3.org/2001/10/synthesis')
        voice = ET.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Jessa24KRUS)')
        voice.text = dataText


        _headers = {"Content-type": "application/ssml+xml", 
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "Authorization": "Bearer " + TTSClass.AccessToken, 
        "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
        "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
        "User-Agent": "ShevaTTS"}

        print "Connecting to Server to Synthesize the Wave"

        TTSClass._connection = httplib.HTTPSConnection("westus.tts.speech.microsoft.com")
        TTSClass._connection.request("POST", "/cognitiveservices/v1", ET.tostring(body),_headers)

        _responseResult = TTSClass._connection.getresponse()
        _data = _responseResult.read()

        print "Status of Request : " + str(_responseResult.status)
        print
        print "Reason for Response : " + _responseResult.reason
        print 
        return _responseResult,_data

    def GetTTSDataLanguage(self, dataText, language, voiceName, gender):
        body = ET.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        body.set('xmlns', 'http://www.w3.org/2001/10/synthesis')
        voice = ET.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        voice.set('name', voiceName)
        voice.text = dataText.translate(None, strg.punctuation)


        _headers = {"Content-type": "application/ssml+xml", 
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "Authorization": "Bearer " + TTSClass.AccessToken, 
        "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
        "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
        "User-Agent": "ShevaTTS"}

        print "Connecting to Server to Synthesize the Wave"

        TTSClass._connection = httplib.HTTPSConnection("westus.tts.speech.microsoft.com")
        TTSClass._connection.request("POST", "/cognitiveservices/v1", ET.tostring(body),_headers)

        _responseResult = TTSClass._connection.getresponse()
        _data = _responseResult.read()

        print "Status of Request : " + str(_responseResult.status)
        print
        print "Reason for Response : " + _responseResult.reason
        print 
        return _responseResult,_data
    
    def TTSSpeak(self,response,data):
        _data= data
        _pyAudio = pyaudio.PyAudio()
        _stream = _pyAudio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        _stream.write(_data)
        _stream.close()
        TTSClass._connection.close()
    
def main():
    testClass = TTSClass()
    #testClass.RecordSpeech()
    #testClass.GetAccessToken()
   # testClass.GetTTSData(' An airport spokesman said more than 110 planes were damaged by hail You have a meal item on your to do list with a description of the fish and ginger sauce is in the fridge warm it up and enjoy')
    st = TTSClass._languageVoices["spanish"]
    text = TranslatorClass().TranslateText(TranslatorClass._translatorLanguage["spanish"],"The current weather has a temperature high of 31 a low of 29 and an average of 30 all in celcius with a humidity of 38")
    response , data = testClass.GetTTSDataLanguage(text, st[1],st[0],st[2])
    testClass.TTSSpeak(response,data)
    

if __name__ == '__main__':
    main()