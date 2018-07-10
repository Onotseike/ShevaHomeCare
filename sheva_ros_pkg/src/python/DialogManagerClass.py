
#######

class DialogManager:
    

    ##### Constants & Variables ########
    _dialogState = {
        "LoginState": "EntryState",
        "DefaultState" : "IdleState",
        "Date.Time" : "GeneralState",
        "Date.Date" : "GeneralState",
        "CallCareGiver": "GeneralState",
        "Exercise": "GeneralState",
        "QueryTodoList": "GeneralState",
        "CRUDTodolist": "GeneralState",
        "Translate.Translate": "GeneralState",
        "Weather.GetCondition": "GeneralState",
        "Weather.GetForecast": "GeneralState",
        "CallInProgess": "CallState",
        "FAQs" : "InfoState"
        }
    _languageOptions = {
        "english" : "en-US",
        "spanish" : "es-ES",
        "italian" : "it-IT"
    }




    ############### Constructor ###################
    def __init__(self,language):
        self._currentState = DialogManager._dialogState.get("DefaultState")
        self._language = language
        self._lastUtteranceResult = ""
        self._lastTextResult = ""
        self._lastLUISResult = ""
        

    ####### Get  and Set Current State ########
    def GetCurentState(self):
        return self._currentState
    
    def SetCurrentSate(self, stateKey):
        self._currentState = DialogManager._dialogState.get(stateKey)
    
    
    ####### Translate to Available Languages ##########
    def TransLateText(self, language, dateText):
        pass
    
    
    
     
    
    
    
    pass