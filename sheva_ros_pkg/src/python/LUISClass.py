#Python 2.7
import httplib, urllib, base64, json


class LUISClass:
    #Variables & Constants
    _intentKeyParams = {
    "CRUDTodolist" : ["crudMethod", "builtin.ordinal", "builtin.number", "itemType", "todoStatus"],
    "CallCareGiver" : [""],
    "Communication.Confirm" : [""],
    "Date.Date" : [""],
    "Date.Time" : [""],
    "Exercise" : ["exerciseType"],
    "LanguageChange" : ["language"],
    "QueryTodoList" : ["crudMethod", "builtin.ordinal", "builtin.number", "itemType"],
    "Translate.Translate" : [""],
    "Weather.GetCondition" : ["Weather.Location"],
    "Weather.GetForecast" : ["Weather.Location"]
    }

    _appId = "da0449d6-b1e6-4e9d-b2df-dd1eba1f7c11"
    _appVersion = "0.1"
    _luisName = "ShevaLUIS"
    _language = "en-US"
    _queryText = 'I want to call jamie'
    _subscriptionKey = "ed82fd027ccd47c3b8ec77f40780124f"

    _requestEndpoint = "westus.api.cognitive.microsoft.com"
    _requestUrl = "/luis/api/v2.0/apps/da0449d6-b1e6-4e9d-b2df-dd1eba1f7c11?%s"

    _requestHeaders = {
        "Content-Type":"application/json",
        "Ocp-Apim-Subscription-Key": _subscriptionKey
    }
    _requestParams = urllib.urlencode({
        'q': _queryText,

        # Optional request parameters, set to default values

        'timezoneOffset': '0',

        'verbose': 'false',

        'spellCheck': 'false',

        'staging': 'false', 
    })

    def __init__(self):
        self._requestEndpoint = LUISClass._requestEndpoint
        self._requestHeaders = LUISClass._requestHeaders
        self._requestParams = LUISClass._requestParams
        self._requestUrl = LUISClass._requestUrl


    def QueryLUIS(self, queryText):
        try:
           self._requestParams =  urllib.urlencode({
               'q': queryText,

                # Optional request parameters, set to default values

                'timezoneOffset': '0',

                'verbose': 'false',

                'spellCheck': 'false',

                'staging': 'false', 
           })
           _connection = httplib.HTTPSConnection(self._requestEndpoint)
           _connection.request("GET","/luis/v2.0/apps/da0449d6-b1e6-4e9d-b2df-dd1eba1f7c11?%s"  % self._requestParams, "{body}", headers=self._requestHeaders)
           _queryResponse = _connection.getresponse()
           _queryResult = _queryResponse.read()
           return json.dumps(json.loads(_queryResult),indent=4, sort_keys=True)
        except Exception as _exception:
            print(_exception)
        finally:
            _connection.close()

    def IntentEntitiesExtractor(self, luisQueryResult):
        result = eval(luisQueryResult)
        #print luisQueryResult
        intentName = result["topScoringIntent"]["intent"]

        entityParams = []
        for entity in result["entities"]:
            if entity["type"] in LUISClass._intentKeyParams[intentName]:
                if entity["type"] !=  "Weather.Location":
                    entityParams.append( {entity["type"]:entity["resolution"].get("values", entity["resolution"].get("value"))[0]})
                else:
                    entityParams.append({entity["type"]: entity["entity"]})
        
        return intentName, entityParams
    

    
def main():
    testClass = LUISClass()
    luisQueryResult = testClass.QueryLUIS("what is the weather in zurich")
    intentName, entityParams = testClass.IntentEntitiesExtractor(luisQueryResult)

    print intentName

    print entityParams


if __name__ == '__main__':
    main()

