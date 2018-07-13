import datetime,time
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
#######


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
        23: "twenty third",
        24: "twenty fourth",
        25: "twenty fifth",
        26: "twenty sixth",
        27: "twenty seventh",
        28: "twenty eighth",
        29: "twenty ninth",
        30: "thirtieth",
        31: " thirty first"
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
            transText = self._translatorObject.TranslateText(
                TranslatorClass._translatorLanguage[self._language], dataText)
            ttsParams = self._ttsObject._languageVoices[self._language]
            ttsResponse, data = self._ttsObject.GetTTSDataLanguage(
                transText, ttsParams[1], ttsParams[0], ttsParams[2])
            while ttsResponse.status != 200:
                self._ttsObject.ReAuthenticate()
                ttsResponse, data = self._ttsObject.GetTTSDataLanguage(
                    transText, ttsParams[1], ttsParams[0], ttsParams[2])
            self._ttsObject.TTSSpeak(ttsResponse, data)

    ########## Intro Greeting #############

    def IntroGreeting(self, username, statSummary):
        # Call TTS Based on Language
        if username == "":
            dataText = DialogManager._greetings[3]
        else:
            dataText = DialogManager._greetings[2] + username
        self.TTSSpeakLanguage(dataText)

        # If state is entry state break else ask what can i do for you
        if self._currentState == DialogManager._dialogState["LoginState"]:
            dataText = statSummary
            # Read Stats
            self.TTSSpeakLanguage(dataText)
            self._currentState = DialogManager._dialogState["DefaultState"]
            return "None",[]

        else:
            dataText = "How can I help you ?"
            # Ask how can i help
            self.TTSSpeakLanguage(dataText)
            self._currentState = DialogManager._dialogState["FAQs"]
            #time.sleep(5)
            transcribedSpeech = self.STTLanguage()
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
            self.TTSSpeakLanguage(dataText)

    ######### State Switching fxns #############

    def StateSwitcher(self, intentName, entityParams):
        if intentName == "CRUDTodolist":
            crud = DialogManager._crudValues.get([entity["crudMethod"] if entity.keys()[0] == "crudMethod" else "set" for entity in entityParams][0])
            item = DialogManager._itemTypeValues.get([entity["itemType"] if entity.keys()[0] == "itemType" else "all" for entity in entityParams][0])
            number = int([entity["builtin.number"] if entity.keys()[0] == "builtin.number" else "1" for entity in entityParams][0])
            ordinal = int([entity["builtin.ordinal"] if entity.keys()[0] == "builtin.ordinal" else "1" for entity in entityParams][0])
            status = DialogManager._todoStatus.get([entity["todoStatus"] if entity.keys()[0] == "todoStatus" else "Open" for entity in entityParams][-1])
            msgArray = [crud, item, number, ordinal, status]
            self.TTSSpeakLanguage("Updating your To do list")
            return intentName, msgArray
        elif intentName == "CallCareGiver":
            # Call Jaime
            return intentName, []
        elif intentName == "Communication.Confirm":
            return intentName, []
        elif intentName == "Date.Date":
            self.GetDateTime(intentName)
            return intentName, []
        elif intentName == "Date.Time":
            self.GetDateTime(intentName)
            return intentName, []
        elif intentName == "Exercise":
            if len(entityParams) == 0: entityParams = [{"exerciseType":"mental"}]
            if entityParams[0].get("exerciseType", "") == "mental":
                 wb.open_new_tab(
                     "https://www.brain-games.co.uk/game/Brain+Trainer")
            else:
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

            crud = DialogManager._crudValues.get([entity["crudMethod"] if entity.keys()[0] == "crudMethod" else "get" for entity in entityParams][0])
            item = DialogManager._itemTypeValues.get([entity["itemType"] if entity.keys()[0] == "itemType" else "all" for entity in entityParams][0])
            number = int([entity["builtin.number"] for entity in entityParams if entity.keys()[0] == "builtin.number"][0])
            ordinal = int([entity["builtin.ordinal"] for entity in entityParams  if entity.keys()[0] == "builtin.ordinal"][0])
            msgArray = [crud, item, number, ordinal]
            self.TTSSpeakLanguage("Querying your To do list")
            return intentName, msgArray
        elif intentName == "Translate.Translate":
            return intentName, []
        elif intentName == "Weather.GetCondition":
            if len(entityParams) == 0: entityParams = [{"Weather.Location":"London"}]
            weatherObservation = self._weatherObject.weather_at_place(
                entityParams[0].get("Weather.Location", "London"))
            weather = weatherObservation.get_weather()
            dataText = "The current weather has a  max temperature of " + str(weather.get_temperature('celsius')["temp_max"]) + ", a min temperature of " + str(weather.get_temperature(
                'celsius')["temp_min"]) + ", an average temperature of " + str(weather.get_temperature('celsius')["temp"]) + " all in celsius and a humidity of " + str(weather.get_humidity())
            self.TTSSpeakLanguage(dataText)
            return intentName, []
        elif intentName == "Weather.GetForecast":
            if len(entityParams) == 0: entityParams = [{"Weather.Location":"London"}]
            location = entityParams[0].get("Weather.Location", "")
            self.TTSSpeakLanguage("Pulling up the weather forecast. please wait")
            wb.open_new_tab(
                "https://www.bing.com/search?q=bing+weather+forecast+" + location)
            return intentName, []
        else:
            # None NO
            return intentName, []

    ####### Translate to Available Languages ##########

    def TransLateText(self, language, dataText):
        textTranslator = TranslatorClass()
        return textTranslator.TranslateText(DialogManager._translatorLanguage[language], dataText)

    ####### STT Language ########
    def STTLanguage(self):
        self._sttObject.RecordSpeech()
        self._sttObject.TranscribeSpeech()
        luisFeed = self._sttObject.GetTranscribedText()
        if self._language == "english":
            return luisFeed
        else:
            return self.TransLateText(self._language,luisFeed)

    def LUISUnderstand(self, transcribedSpeech):
        luisQueryResult = self._luisObject.QueryLUIS(transcribedSpeech)
        #print luisQueryResult
        intentName, entityParams = self._luisObject.IntentEntitiesExtractor(luisQueryResult)

        print intentName
        print entityParams
        return intentName, entityParams
