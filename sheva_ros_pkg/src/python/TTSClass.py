import httplib, urllib, json
import pyaudio, wave
from xml.etree import ElementTree as ET
from os.path import join, dirname


class TTSClass:
    #Class for all things relating to Speech Services.

    #Variables
    apiKey = "569cb77237894b4581bebd1e84de94ff"
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
    testClass.GetTTSData(' An airport spokesman said more than 110 planes were damaged by hail. You have a meal item on your to do list with a description of: the fish and ginger sauce is in the fridge, warm it up and enjoy.')
    

if __name__ == '__main__':
    main()