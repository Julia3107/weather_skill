
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import requests

__author__ = "Julia"

def makeRequest(led, action):


    if led =="dull red":
        led = "bred"
    elif led =="dull green":
        led = "bgreen"

    if action == "on":
        action = "ON"
    elif action == "off":
        action == "OFF"

    #if led == "all":
        #allLED(action)
    #else:
        #requestNormal(led, action)

    return led, action

def allLED(action):
    urlRed = "http://192.168.178.29/rest/items/red"
    urlGreen = "http://192.168.178.29/rest/items/green"
    urlBgreen = "http://192.168.178.29/rest/items/bgreen"
    urlBred = "http://192.168.178.29/rest/items/bred"

    try:
        responseRed = requests.post(urlRed, data=action)
        print(responseRed)

        responseGreen = requests.post(urlGreen, data=action)
        print(responseGreen)

        responseBgreen = requests.post(urlBgreen, data=action)
        print(responseBgreen)

        responseBred = requests.post(urlBred, data=action)
        print(responseBred)

    except KeyError:
        pass

    return responseRed, responseGreen, responseBred, responseBgreen

def requestNormal(led, action):
        url = "http://192.168.178.29/rest/items/" + led

        try:
            response = requests.post(url, data=action)
        except KeyError:
            pass

        return response


class ArduinoLEDControlSkill(MycroftSkill):

    def __init__(self):
        super(ArduinoLEDControlSkill, self).__init__(name="ArduinoLEDControlSkill")
        

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'

    def initialize(self):

        # Intent on/off
        on_off_intent = IntentBuilder("On_Off_Intent").require("action").require("ledName").require("actionName").build()
        self.register_intent(on_off_intent, self.handle_on_off_intent)

        #Intent dimmer
        brightness_value_intent = IntentBuilder("Brightness_Value_Intent").require("action").require("ledName").require("brightnessValue").build()
        self.register_intent(brightness_value_intent, self.handle_brightness_value_intent)

    def handle_on_off_intent(self, message):

        ledMessage = message.data.get("ledName")
        actionMessage = message.data.get("actionName")

        led, action = makeRequest(ledMessage, actionMessage)

        if led == "all":
            resRed, resGreen, resBred, resBgreen = allLED(action)
            if resRed.status_code == 200 and resGreen.status_code == 200 and resBred.status_code == 200 and resBgreen.status_code == 200:
                self.speak_dialog("OnOff", {"name": ledMessage, "status": actionMessage})
            else:
                self.speak_dialog("request.fail")
        else:
            res = requestNormal(led, action)
            if res.status_code == 200:
                self.speak_dialog("OnOff", {"name": ledMessage, "status": actionMessage})
            else:
                self.speak_dialog("request.fail")

    def handle_brightness_value_intent(self, message):

        ledMessage = message.date.get("ledName")
        valueMessage = message.date.get("brightnessValue")

        led, action = makeRequest(ledMessage, valueMessage)

        if led == "all":
            resRed, resGreen, resBred, resBgreen = allLED(action)
            if resRed.status_code == 200 and resGreen.status_code == 200 and resBred.status_code == 200 and resBgreen.status_code == 200:
                self.speak_dialog("Dim", {"name": ledMessage, "status": valueMessage})
            else:
                self.speak_dialog("request.fail")
        else:
            res = requestNormal(led, action)
            if res.status_code == 200:
                self.speak_dialog("Dim", {"name": ledMessage, "status": valueMessage})
            else:
                self.speak_dialog("request.fail")


    def stop(self):
        pass


def create_skill():
    return ArduinoLEDControlSkill()
