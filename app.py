import os
import requests
from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import SerpApiSearches
import route

load_dotenv()

app = Flask(__name__)

HELP_STR1 = 'Welcome to *Know The Way*!\n' \
            'This bot helps to get the best route for where you want to go!\n' \
            '*Please follow the steps to start using the bot:*\n' \
            'To use get the best route:\n' \
            "1. Enter the command: _dawae route_\n" \
            "2. The bot will then ask for the list of locations and help you plan the optimal route by distance\n" \
            'To use a location to get the suggested destinations:\n' \
            "1. Enter the command: _suggestions_ followed by ```your location```\n" \
            "2. The bot will then use the location provided to return any destinations of interest found\n" \
            'To *view this instruction message* again, you can send a message containing the following ' \
            'keywords: _instructions_, _help_ , _how to_\n' \
            'Thanks for using Know The Way!'

Bonus_Suggestion_Feature =
HELP_STR2 = 'Invalid command.\n' \
            'To view this instruction message again, you can send a message containing the following ' \
            'keywords:\ninstructions, help , how to'

'''
0 - not active
1 - collecting locale for precise search (aka country)
2 - collecting travel method
3 - collecting locations
4 - confirming returning order
5 - 
'''
route_parsing = 0
destinations = []

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

# Recieve the message from Twilio
@app.route('/message', methods=['POST'])
def reply():
    # Parse out the information from the Twilio message recieved
    sender = request.form.get('From')
    message = request.form.get('Body').lower()

    # media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')

    if route_parsing == 0:
        print("hi")

    if 'dawae' in message:
        print('dawae')
        keywords = message.replace('dawae ', '')

        if keywords == '':
            return respond('No search term given. Please try again with keywords.')
        elif "route" in keywords:
            info = "What country are the locations in?"
            route_parsing = 1
            return respond(info)
    elif "suggestions" in message:
        print("suggestions")
        keywords = message.replace('suggestions ', "")
        info = SerpApiSearches.search_location(keywords)

        return respond(info)
    elif 'help' in message or 'instruction' in message or 'how to' in message:
        print('help')
        return respond(HELP_STR1)

    # elif media_url:

    else:
        return respond(HELP_STR2)