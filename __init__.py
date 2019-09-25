
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import json
import requests

__author__ = "Julia Albert"

# Funktion zum Verwendung der API
def getWeather(location):
    url = "http://api.worldweatheronline.com/premium/v1/weather.ashx?key=985ef9c3a7bd499587c115157192509&q=" + location + "&tp=3&num_of_days=1&cc=yes&format=json"

    try:
        response = requests.get(url)

    except KeyError:
        pass

    return response

# Skillklasse
class WeatherSkill(MycroftSkill):

    # Konstruktor
    def __init__(self):
        super(WeatherSkill, self).__init__(name="WeatherSkill")

    # Intent definieren
    def initialize(self):

        weather_intent = IntentBuilder("Weather_Intent").require("action").require("location").build()
        self.register_intent(weather_intent, self.handle_weather_intent)

    # Intent-handler für Wetter
    def handle_weather_intent(self, message):
        locationMessage = message.data.get("location")

        res = getWeather(locationMessage)

        if res.status_code == 200:
            data = json.loads(res.text)

            temp = data["data"]
            temp = temp["current_condition"]
            temp = temp[0]
            temp = temp["weatherDesc"]
            temp = temp[0]
            temp = temp["value"]

            weatherDesc = temp

            self.speak_dialog("weather",{"location": locationMessage, "weather": weatherDesc} )

        else:
            self.speak_dialog("fail")

    # Ausführung bei Stop-Intent (hier keine Funktion)
    def stop(self):
        pass

# Skill erstellen
def create_skill():
    return WeatherSkill()
