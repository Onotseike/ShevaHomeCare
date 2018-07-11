import datetime, webbrowser as wb, pyowm
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
        "CallInProgress": "CallState",
        "FAQs" : "InfoState"
        }
    _languageOptions = {
        "english" : "en-US",
        "spanish" : "es-ES",
        "italian" : "it-IT"
        }
    _greetings = {
        1: "Hi ",
        2: "Hello ",
        3: "Hello love"
        }
    _days = {
        "monday" : 1,
        "tuesday" : 2,
        "wednesday" : 3,
        "thursday" : 4,
        "friday" : 5,
        "saturday" : 6,
        "sunday" : 7
        }
    _month = {
        1 : "january",
        2 : "february",
        3 : "march",
        4 : "april",
        5 : "may",
        6 : "june",
        7 : "july",
        8 : "august",
        9 : "september",
        10 : "october",
        11 : "november",
        12 : "december"
        }
    _dayNumber = {
        1 : "first",
        2 : "second",
        3 : "third",
        4 : "fourth",
        5 : "fifth",
        6 : "sixth", 
        7 : "seventh", 
        8 : "eighth",
        9 : "ninth",
        10 : "tenth",
        11 : "eleventh",
        12 : "twelfth",
        13 : "thirteenth",
        14 : "fourteenth",
        15 : "fifteenth",
        16 : "sixteenth",
        17 : "seventeenth",
        18 : "eighteenth",
        19 : "nineteenth",
        20 : "twentieth",
        21 : "twenty first",
        22 : "twenty second",
        23 : "twenty third",
        24 : "twenty fourth",
        25 : "twenty fifth",
        26 : "twenty sixth",
        27 : "twenty seventh",
        28 : "twenty eighth",
        29 : "twenty ninth",
        30 : "thirtieth",
        31 :" thirty first"
        }

    ############### Constructor ###################
    def __init__(self,language):
        self._currentState = DialogManager._dialogState.get("DefaultState")
        self._language = language
        self._lastUtteranceResult = ""
        self._lastTextResult = ""
        self._lastLUISResult = ""

        self._weatherObject = pyowm.OWM("955ad4192620bbe51f557e76c251df2b")
    
    

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
        if self._language == DialogManager._languageOptions["english"]:
            #Call TTS English                
            pass

        else:

            #Call TTS Language                
            pass

    ########## Intro Greeting #############
    def IntroGreeting(self, username, statSummary):
        #Call TTS Based on Language 
        dataText = DialogManager._greetings + username
        self.TTSSpeakLanguage(dataText)
        
        ###### If state is entry state break else ask what can i do for you
        if self._currentState == DialogManager._dialogState["LoginState"]:
            dataText = statSummary
            #Read Stats
            self.TTSSpeakLanguage(dataText)           
            self._currentState = DialogManager._dialogState["DefaultState"]
            return self._currentState
            
        else:
            dataText = "How can I help you ?"
            #Ask how can i help
            self.TTSSpeakLanguage(dataText)
            # Record Speech, Transcribe, send to LUIS, call state Switcher
        
        return self._currentState

    def GetDateTime(self, intentName):
        currentDate = datetime.datetime.now()
        if intentName == "Date.Time":
            result = (currentDate.hour,currentDate.minute)
            dataText = "The time is " + result[0] + " " + result[1]
            self.TTSSpeakLanguage(dataText)
        else:
            result = (currentDate.year, currentDate.month, currentDate.day, currentDate.weekday+1)
            dataText = "Today is " + " " + DialogManager._days[result[3]] + " the " + DialogManager._dayNumber[result[2]] + " of " + DialogManager._month[result[1]] + " " + result[0] 
            self.TTSSpeakLanguage(dataText)
        

    ######### State Switching fxns
    def StateSwitcher(self, intentName, entityParams):
        if intentName == "CRUDTodolist":
            ##params [ordinal_resolution value, number_resolution value, item_type,status]
            #create message to send query needs
            if "meal" in entityParams[2]:
                #send [ordinal,number, enum value for meal]
                pass
            elif "drug" in entityParams[2]:
                #send [ordinal,number, enum value for drug]
                pass
            elif "exercise" in entityParams[2]:
                #send [ordinal,number, enum value for exercise]
                pass
            elif "general" in entityParams[2]:
                #send [ordinal,number, enum value for misc]
                pass
            else:
                #No preference
                pass
           
            #Resolve status
            if "Uncompleted" in entityParams[3] or "Not" in entityParams[3]:
                #set status not done
                pass
            elif "Done" in entityParams[3] or "Completed" in entityParams[3] or "Finished" in entityParams[3] or "Close" in entityParams[3]:
                #set as done
                pass
            else:
                #set as in progress
                pass
           
            self.TTSSpeakLanguage("Updating your To do list")
        elif intentName == "CallCareGiver":
            #Call Jaime
            pass
        elif intentName == "Communication.Confirm":
            pass
        elif intentName == "Date.Date":
            self.GetDateTime(intentName)
        elif intentName == "Date.Time":
            self.GetDateTime(intentName)
        elif intentName == "Exercise":
            if entityParams[0] in ["mental", "brain", "non-physical", "non physical", "brain games", "games"]:
                 wb.open_new_tab("https://www.brain-games.co.uk/game/Brain+Trainer")
            else:
                wb.open_new_tab("https://www.nhs.uk/Tools/Documents/NHS_ExercisesForOlderPeople.pdf")            
        elif intentName == "LanguageChange":
            self._language = DialogManager._languageOptions[entityParams[0]]
            #send language data to web app and refresh page to reflect change
        elif intentName == "QueryTodoList":
            ##params [ordinal_resolution value, number_resolution value, item_type]
            #create message to send query needs
            if "meal" in entityParams[2]:
                #send [ordinal,number, enum value for meal]
                pass
            elif "drug" in entityParams[2]:
                #send [ordinal,number, enum value for drug]
                pass
            elif "exercise" in entityParams[2]:
                #send [ordinal,number, enum value for exercise]
                pass
            elif "general" in entityParams[2]:
                #send [ordinal,number, enum value for misc]
                pass
            else:
                #No preference
                pass
            self.TTSSpeakLanguage("Querying your To do list")
        elif intentName == "Translate.Translate":
            pass
        elif intentName == "Weather.GetCondition":
            weatherObservation =self._weatherObject.weather_at_place(entityParams[0])
            weather = weatherObservation.get_weather()
            dataText = "The current weather has a  max temperature of " + str(weather.get_temperature('celsius')["temp_max"]) + ", a min temperature of " + str(weather.get_temperature('celsius')["temp_min"]) + ", an average temperature of " + str(weather.get_temperature('celsius')["temp"]) + " all in celsius and a humidity of " + str(weather.get_humidity())
            self.TTSSpeakLanguage(dataText)
        elif intentName == "Weather.GetForecast":
            wb.open_new_tab("https://www.bing.com/search?q=bing+weather+forecast&form=EDGTCT&qs=AS&cvid=63b02838def94778a1900798c6c751b5&refig=44fadddfa5f342f0d3a4a6f4facf0ef3&cc=US&setlang=en-US")
        else:
            #None NO
            pass






    ####### Translate to Available Languages ##########
    def TransLateText(self, language, dateText):
        pass
    
    
    
     
    
    
    
    pass