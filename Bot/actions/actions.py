# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from pynput.keyboard import Key, Listener
from logging import Handler
from typing import Any, Text, Dict, List
from rasa.core.channels.socketio import *
from rasa_sdk import Action , Tracker
from rasa_sdk import events
from rasa_sdk.events import (
    ConversationPaused,
    ConversationResumed,
    UserUtteranceReverted
)
from rasa_sdk.executor import CollectingDispatcher

from random import randint
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import socketio
from time import sleep # just used for timing the messages

#load environment variable

# env_path = Path(".")/".env"
# load_dotenv(dotenv_path = env_path)

# socket programming

sio = socketio.Client()
# sio.wait()  # if you want server to always connected with client
@sio.event
def connect():
    print('Connection established with server to send message data.')

def send_msg(msg):
    print("sending")
    sio.emit('message', msg)

@sio.event
def disconnect():
    print('Disconnected from websocket! Cannot send message data.')

# @sio.call
# def callme():
#     pass

  
# message = {"user":"neelkant", "message":"I am a good boy"}
# list of messages to send

# while True:
#     socket.on('message', message_handler)

#<=======================================Problem to be worked on ================================>

# to use this mssg which we are getting from admin and dispatch it to our user in chatbot interface
# if we are able to get the mssg out side the message_handler and used it in Action Default fallback may be we can solve the issue
@sio.on('message')
def message_handler(mssg):
    print(mssg)
    
sio.connect('http://localhost:3000')

#<============================== Action for Human handoff ========================>

class ActionHumanHandoff(Action):
    # global my_message
    
    """
    human in the loop action
    """
    def name(self) -> Text:
        return "action_human_handoff"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # sio.disconnect()
        
        dispatcher.utter_message(text="Hello i am Neelkant I am you live assistant")
        # events.append(ConversationPaused())
        msg = {
            "user": "User",
            "message": tracker.latest_message['text']
        }
        send_msg(msg)
        # dispatcher.utter_message(my_message)

        return []
    
#<==============================================================================================>


sio.on('message', message_handler) 

#<====================== Action using fall back policy ==========================================>
'''Currently i am using fallback policy which sometimes lead to open the bot conversation if it find the
the intent prediction above the threshold.

Need to be solved using the slot 

- suppose we make a slot /handoff with initial value false, when we have a human handoff action we will set the slot to true 
- Now since our slot is true we can make a policy HumanHandoff with highest priority and set the policy action to actionfallback.
Now every message will come in Action fall back and we will continue all our message to the admin.
'''

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        msg = {
            "user": "User",
            "message": tracker.latest_message['text']
        }
        send_msg(msg)

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]

