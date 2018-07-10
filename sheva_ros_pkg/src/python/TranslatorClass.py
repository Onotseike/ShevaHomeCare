import httplib, urllib, uuid, json

class TranslatorClass:

    def __init__(self):
        self.subscriptionKey = "629dcd9ccd724db2bf734064980133fe"
        self.host = "api.cognitive.microsofttranslator.com"
        self.path = "/translate?api-version=3.0"
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.subscriptionKey,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
            }
        self.params = ""
    

    def TranslateText(self, language, dataText):
        self.params = "&to=" + language

        _requestBody = [{ 'Text' : dataText}]
        _requestBody = json.dumps(_requestBody, ensure_ascii=False).encode('utf-8')
        
        _connection = httplib.HTTPSConnection(self.host)
        _connection.request("POST",url=self.path+self.params, body=_requestBody,headers=self.headers)

        _responseResult = _connection.getresponse()
        result = _responseResult.read()
        result = eval(result)[0]["translations"][0]["text"]
        return result
        


def main():
    testClass = TranslatorClass()
    result =testClass.TranslateText("es", "Hello, My Name is Paula")
    
    print result

if __name__ == '__main__':
    main()
