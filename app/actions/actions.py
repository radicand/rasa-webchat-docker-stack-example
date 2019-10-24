# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from actions import cities
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List

import world_bank_data as worldbank

from pprint import pprint
from datetime import datetime, timedelta
import pytz
import time
import re
import logging
import json
from functools import reduce
import random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

cityData = cities.Cities()


def getUserInfo(tracker):
    filtered_events = filter(lambda evt: 'event' in evt and evt['event'] ==
                             'user' and 'metadata' in evt and 'userInfo' in evt['metadata'], tracker.events)
    events = list(filtered_events)
    userInfo = events.pop()['metadata']['userInfo']
    return json.loads(userInfo)


class ActionHelloWorld(Action):
    # not used
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")

        return []


# class ActionGetCountryInfo(Action):

#     def name(self) -> Text:
#         return "action_country_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             userInfo = getUserInfo(tracker)
#         except Exception as e:
#             dispatcher.utter_message(
#                 'Sorry, something went wrong while figuring out who you are.')
#             # determine how to abort the conversation at this point.
#             logger.exception(e)
#             return []

#             if results == 0:
#                 dispatcher.utter_message(
#                     'Hmm, I wasn\'t able to find anything matching `' + term + '`. Can you rephrase it?')

#         except Exception as e:
#             dispatcher.utter_message(
#                 'Sorry, something went wrong while getting content for you.')
#             logger.exception(e)

#         return []


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cdata = None
        tzdata = None

        logger.debug(str(tracker))

        city = tracker.get_slot('city')
        dispatcher.utter_message('City: ' + str(city))
        if city != None:
            cdata = cityData.findCity(city)
            if cdata:
                tzdata = pytz.timezone(cdata['timezone'])
            else:
                dispatcher.utter_message(
                    'Sorry, I don\'t know where ' + city + ' is. Can you spell it differently?')

        try:
            nowtime = datetime.utcnow()

            if tzdata:
                nowtime = tzdata.localize(nowtime)

            t = nowtime.strftime("%H:%M (%b %d)")

            if cdata:
                dispatcher.utter_message(
                    "The current time in " + cdata['name'] + " is " + t)
                dispatcher.utter_message(
                    "By the way, did you know that city's population is " +
                    "{:,}".format(cdata['population']) + "?"
                )
            else:
                dispatcher.utter_message(
                    "The current time here (I didn't understand the city if you said one) is " + t)

        except Exception as e:
            dispatcher.utter_message(
                'Sorry, something went wrong while figuring out the current time.')
            logger.exception(e)

        return []


class ActionWhoAreYou(Action):
    def name(self) -> Text:
        return "action_who_are_you"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            userInfo = getUserInfo(tracker)
        except Exception as e:
            dispatcher.utter_message(
                'Sorry, something went wrong while figuring out who you are.')
            logger.exception(e)
            return []

            message = "You are " + \
                userInfo['name'] + " and you're currently at " + userInfo['location'] + \
                '. If that does not seem right, check your userInfo payload in index.html :)'

            dispatcher.utter_message(message)

        except Exception as e:
            dispatcher.utter_message(
                'Sorry, something went wrong while figuring out your info.')
            logger.exception(e)

        return []
