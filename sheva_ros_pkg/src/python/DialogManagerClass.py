import datetime,time,os
import webbrowser as wb
import pyowm
import pyaudio
import wave
from xml.etree import ElementTree as ET
from os.path import join, dirname
from TranslatorClass import TranslatorClass
from TTSClass import TTSClass
from STTClass import STTClass
from LUISClass import LUISClass
########
#roslaunch rosbridge_server rosbridge_websocket.launch

class DialogManager:

    ##### Constants & Variables ########
    _dialogState = {
        "LoginState": "EntryState",
        "DefaultState": "IdleState",
        "Date.Time": "GeneralState",
        "Date.Date": "GeneralState",
        "CallCareGiver": "GeneralState",
        "Exercise": "GeneralState",
        "QueryTodoList": "GeneralState",
        "CRUDTodolist": "GeneralState",
        "Translate.Translate": "GeneralState",
        "Weather.GetCondition": "GeneralState",
        "Weather.GetForecast": "GeneralState",
        "CallInProgress": "CallState",
        "FAQs": "InfoState"
    }
    _languageOptions = {
        "english": "en-US",
        "spanish": "es-ES",
        "italian": "it-IT"
    }
    _translatorLanguage = {
        "english": "en",
        "spanish": "es",
        "italian": "it"
    }
    _greetings = {
        1: "Hi ",
        2: "Hello ",
        3: "Hello love"
    }
    _days = {
        0:"monday",
        1:"tuesday",
        2:"wednesday",
        3:"thursday",
        4:"friday",
        5:"saturday",
        6:"sunday"
    }
    _month = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december"
    }
    _dayNumber = {
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "sixth",
        7: "seventh",
        8: "eighth",
        9: "ninth",
        10: "tenth",
        11: "eleventh",
        12: "twelfth",
        13: "thirteenth",
        14: "fourteenth",
        15: "fifteenth",
        16: "sixteenth",
        17: "seventeenth",
        18: "eighteenth",
        19: "nineteenth",
        20: "twentieth",
        21: "twenty first",
        22: "twenty second",
        23: "twenty-third",
        24: "twenty-fourth",
        25: "twenty-fifth",
        26: "twenty-sixth",
        27: "twenty-seventh",
        28: "twenty-eighth",
        29: "twenty-ninth",
        30: "thirtieth",
        31: " thirty-first"
    }
    _crudValues = {
        "get": 0,
        "set": 1
    }
    _itemTypeValues = {
        "meal": 0,
        "exercise": 1,
        "drug": 2,
        "general": 3,
        "all": 4
    }
    _todoStatus = {
        "Open": 0,
        "InProgress": 1,
        "Close": 2
    }

    ############### Constructor ###################
    def __init__(self, language):
        self._currentState = DialogManager._dialogState.get("DefaultState")
        self._language = language
        self._lastUtteranceResult = ""
        self._lastTextResult = ""
        self._lastLUISResult = ""

        self._weatherObject = pyowm.OWM("955ad4192620bbe51f557e76c251df2b")
        self._ttsObject = TTSClass()
        self._translatorObject = TranslatorClass()
        self._sttObject = STTClass(language)
        self._luisObject = LUISClass()

    ####### Get  and Set Current State ########

    def GetCurentState(self):
        return self._currentState

    def SetCurrentSate(self, stateKey):
        self._currentState = DialogManager._dialogState.get(stateKey)

    ########## Get and Set Language Options ############

    def GetCurrentLanguage(self):
        return self._language

    def SetCurrentLanguage(self, language):
        self._language = language

    def TTSSpeakLanguage(self, dataText):
        if self._language == "english":
            # Call TTS English
            ttsResponse, data = self._ttsObject.GetTTSData(dataText)
            while ttsResponse.status != 200:
                self._ttsObject.ReAuthenticate()
                ttsResponse, data = self._ttsObject.GetTTSData(dataText)
            self._ttsObject.TTSSpeak(ttsResponse, data)

        else:
            # Call TTS Language
            import string
            txt =  dataText.translate(None, string.punctuation)
            print txt
            transText = self._translatorObject.TranslateText(
                TranslatorClass._translatorLanguage[self._language], txt)
            ttsParams = self._ttsObject._languageVoices[self._language]
            ttsResponse, data = self._ttsObject.GetTTSDataLanguage(
                transText, ttsParams[1], ttsParams[0], ttsParams[2])
            while ttsResponse.status != 200:
                self._ttsObject.ReAuthenticate()
                ttsResponse, data = self._ttsObject.GetTTSDataLanguage(
                    transText, ttsParams[1], ttsParams[0], ttsParams[2])
            self._ttsObject.TTSSpeak(ttsResponse, data)
   
    def TTSSpeakEnglish(self, dataText):
        ttsResponse, data = self._ttsObject.GetTTSData(dataText)
        while ttsResponse.status != 200:
            self._ttsObject.ReAuthenticate()
            ttsResponse, data = self._ttsObject.GetTTSData(dataText)
        self._ttsObject.TTSSpeak(ttsResponse, data)

    ########## Intro Greeting #############

    def IntroGreeting(self, username, statSummary):
        # Call TTS Based on Language
        if username == "":
            dataText = DialogManager._greetings[3] + ". "
        else:
            dataText = DialogManager._greetings[2] + username + ". "
        #self.TTSSpeakLanguage(dataText)

        # If state is entry state break else ask what can i do for you
        if self._currentState == DialogManager._dialogState["LoginState"]:
            dataText += statSummary
            # Read Stats
            self.TTSSpeakLanguage(dataText)
            self._currentState = DialogManager._dialogState["DefaultState"]
            return "None",[]

        else:
            dataText += "How can I help you ?"
            # Ask how can i help
            self.TTSSpeakLanguage(dataText)
            self._currentState = DialogManager._dialogState["FAQs"]
            #time.sleep(5)
            transcribedSpeech = self.STTLanguage()
            if transcribedSpeech == "":
                self.TTSSpeakLanguage("Sorry I did not catch that. If you need me, just toggle the start speech button on your Dashboard.")
                intentName, msgArray = "None",[]
            else:
                intent, entities = self.LUISUnderstand(transcribedSpeech)
                intentName, msgArray = self.StateSwitcher(intent, entities)
            return intentName, msgArray


            # Record Speech, Transcribe, send to LUIS, call state Switcher        

    def GetDateTime(self, intentName):
        currentDate = datetime.datetime.now()
        if intentName == "Date.Time":
            result = (currentDate.hour, currentDate.minute)
            dataText = "The time is " + str(result[0]) + " " + str(result[1])
            self.TTSSpeakLanguage(dataText)
        else:
            result = (currentDate.year, currentDate.month,
                      currentDate.day, currentDate.weekday())
            dataText = "Today is " + " " + DialogManager._days[result[3]] + " the " + DialogManager._dayNumber[result[2]] + " of " + DialogManager._month[result[1]] + " " + str(result[0])
           # import string
            #dataText = dataText.translate(None, string.punctuation)
            #print dataText
            self.TTSSpeakLanguage(dataText)

    ######### State Switching fxns #############

    def StateSwitcher(self, intentName, entityParams):
        if intentName == "CRUDTodolist":
            crud = DialogManager._crudValues.get(next(iter( [entity.get("crudMethod") for entity in entityParams if "crudMethod" in entity.keys()]),"set"))
            
            item = DialogManager._itemTypeValues.get(next(iter( [entity.get("itemType") for entity in entityParams if "itemType" in entity.keys()]),"all"))

            number = int(next(iter( [entity.get("builtin.number") for entity in entityParams if "builtin.number" in entity.keys()]),"0"))

            ordinal = int(next(iter( [entity.get("builtin.ordinal") for entity in entityParams if "builtin.ordinal" in entity.keys()]),"1"))

            status = DialogManager._todoStatus.get(next(iter([entity.get("todoStatus") for entity in entityParams if "todoStatus" in entity.keys()]),"Close"))

            if number == 0 and ordinal != 0:
                number = ordinal
                ordinal = 1

            msgArray = [crud, item, number, ordinal, status]
            self.TTSSpeakLanguage("Updating your To do list. Please wait")
            return intentName, msgArray
        elif intentName == "CallCareGiver":
            # Call Jaime
            dir_path = os.path.dirname(os.path.realpath(__file__))
            scriptsDir = os.path.join(dir_path, "..","..","scripts","ShevaMainPage.html")
            #print(scriptsDir)
            self.TTSSpeakLanguage("Attempting to connect you to your Care Giver, please wait")
            wb.open_new_tab(scriptsDir)
            return intentName, []
        # elif intentName == "Communication.Confirm":
        #     return intentName, []
        elif intentName == "Date.Date":
            self.GetDateTime(intentName)
            return intentName, []
        elif intentName == "Date.Time":
            self.GetDateTime(intentName)
            return intentName, []
        elif intentName == "Exercise":
            if len(entityParams) == 0: entityParams = [{"exerciseType":"mental"}]
           
            if entityParams[0].get("exerciseType", "") == "mental":
                 self.TTSSpeakLanguage("Redirecting you to a Brain Game Website Please wait")
                 wb.open_new_tab(
                     "https://www.brain-games.co.uk/game/Brain+Trainer")
            else:
                self.TTSSpeakLanguage("Redirecting you to a exercise resource please wait")
                wb.open_new_tab(
                    "https://www.nhs.uk/Tools/Documents/NHS_ExercisesForOlderPeople.pdf")
            return intentName, []
        elif intentName == "LanguageChange":
            if len(entityParams) == 0: entityParams = [{"language":"english"}]
            self._language = entityParams[0].get("language", "english")
            # send language data to web app and refresh page to reflect change
            self.TTSSpeakLanguage("Updating your language preferences, please wait")
            return intentName, [self._language]
        elif intentName == "QueryTodoList":
            # params [ordinal_resolution value, number_resolution value, item_type]
            # create message to send query needs          
            
            crud = DialogManager._crudValues.get(next(iter( [entity.get("crudMethod") for entity in entityParams if "crudMethod" in entity.keys()]),"get"))
            
            item = DialogManager._itemTypeValues.get(next(iter( [entity.get("itemType") for entity in entityParams if "itemType" in entity.keys()]),"all"))

            number = int(next(iter( [entity.get("builtin.number") for entity in entityParams if "builtin.number" in entity.keys()]),"0"))

            ordinal = int(next(iter( [entity.get("builtin.ordinal") for entity in entityParams if "builtin.ordinal" in entity.keys()]),"1"))
            if number == 0 and ordinal != 0:
                number = ordinal
                ordinal = 1
            msgArray = [crud, item, number, ordinal]
            self.TTSSpeakLanguage("Querying your To do list")
            return intentName, msgArray
        elif intentName == "Weather.GetCondition":
            if len(entityParams) == 0: entityParams = [{"Weather.Location":"London"}]
            self.TTSSpeakLanguage("Colatting current weather results, Please wait")
            weatherObservation = self._weatherObject.weather_at_place(
                entityParams[0].get("Weather.Location", "London"))
            weather = weatherObservation.get_weather()
            dataText = "The current weather has a temperature high of  " + str(int(weather.get_temperature('celsius')["temp_max"])) + ", a low of " + str(int(weather.get_temperature(
                'celsius')["temp_min"])) + ", and an average of " + str(int(weather.get_temperature('celsius')["temp"])) + ", all in celsius and a humidity of " + str(weather.get_humidity())
            
            self.TTSSpeakLanguage(dataText)
            return intentName, []
        elif intentName == "Weather.GetForecast":
            if len(entityParams) == 0: entityParams = [{"Weather.Location":"London"}]
            location = entityParams[0].get("Weather.Location", "")
            self.TTSSpeakLanguage("Pulling up updates for the weather, please wait")
            wb.open_new_tab(
                "https://www.bing.com/search?q=bing+weather+forecast+" + location)
            return intentName, []
        else:
            # None NO
            self.TTSSpeakLanguage("My Apologies, I am not trained to understand that request yet")
            return intentName, []

    ####### Translate to Available Languages ##########

    def TransLateText(self, language, dataText):
        textTranslator = TranslatorClass()
        return textTranslator.TranslateText(DialogManager._translatorLanguage[language], dataText)

    ####### STT Language ########
    def STTLanguage(self):
        self._sttObject.RecordSpeech()
        self._sttObject.TranscribeSpeech()
        import unidecode
               
        txt =  unidecode.unidecode(self._sttObject.GetTranscribedText())
        print txt
        luisFeed = txt #self._sttObject.GetTranscribedText()
        if luisFeed != "" :
            if self._language == "english":
                 return luisFeed
            else:
                return self.TransLateText(self._language,luisFeed)
        else:
            return ""
        

    def LUISUnderstand(self, transcribedSpeech):
        luisQueryResult = self._luisObject.QueryLUIS(transcribedSpeech)
        #print luisQueryResult
        intentName, entityParams = self._luisObject.IntentEntitiesExtractor(luisQueryResult)

        print intentName
        print entityParams
        return intentName, entityParams
