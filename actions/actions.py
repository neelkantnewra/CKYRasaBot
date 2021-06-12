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

env_path = Path(".")/".env"
load_dotenv(dotenv_path = env_path)

# socket programming

sio = socketio.Client()
# sio.wait()
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
@sio.on('message')
def message_handler(mssg):
    # dispatcher = CollectingDispatcher()
    # dispatcher.utter_message(text=msg["message"])
    # print(mssg)
    # global my_message
    # my_message = mssg
    # sio.disconnect()
    # sio.connect("http://localhost:5005")
    # sio.emit('message',mssg)
    print(mssg)
    
        # socket.emit('message', msg)
    # CollectingDispatcher.utter_message(text = msg['message'])

# def show(key,msg):
#     if key == Key.ENTER:
#         send_msg(msg)
sio.connect('http://localhost:3000')

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

sio.on('message', message_handler) 

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

