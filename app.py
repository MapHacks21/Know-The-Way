import os
import requests
from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import SerpApiSearches
import route
import json
import staticmap


# defaultData = {
#   "route_parsing": 0,
#   "location": "",
#   "transport": "walk",
#   "destinations": []
# }
#
# with open('data.json', 'w') as outfile:
#     json.dump(defaultData, outfile)
#
# with open("data.json") as json_file:
#     data = json.load(json_file)
#     print(data)


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

HELP_STR2 = 'Invalid command.\n' \
            'To view this instruction message again, you can send a message containing the following ' \
            'keywords:\ninstructions, help , how to'

'''
0 - not active
1 - collecting locale for precise search (aka country)
2 - collecting travel method
3 - collecting locations
4 - confirming returning image
5 - 
'''

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

    # check if the corresponding json exists for the sender
    fname = sender + ".json"
    if os.path.isfile(fname):
        # read the json storing previous message info
        with open(fname) as json_file:
            data = json.load(json_file)
            print(data)
            route_parsing = data["route_parsing"]
            location = data["location"]
            transport = data["transport"]
            destinations = data["destinations"]
    else:
        route_parsing = 0
        location = ""
        transport = "walk"
        destinations = []
        updateJsonData(fname, route_parsing, location, transport, destinations)

    print(f'{sender} sent {message}')

    print(route_parsing)
    if "cancel" in message:
        route_parsing = 0
        updateJsonData(fname, route_parsing, location, "walk", destinations)
        return respond("Input cancelled")
    elif route_parsing == 1:
        print("collecting location")
        if message:
            location = message
            route_parsing = 2
            updateJsonData(fname, route_parsing, location, transport, destinations)
            return respond("What is your travel method (car, walk, cycle, transit)?")
        else:
            return respond("Please input location")
    elif route_parsing == 2:
        if "cycle" in message:
            route_parsing = 3
            updateJsonData(fname, route_parsing, location, "cycle", destinations)
            return respond("List the locations you want to visit today (comma separated):")
        elif "walk" in message:
            route_parsing = 3
            updateJsonData(fname, route_parsing, location, "walk", destinations)
            return respond("List the locations you want to visit today (comma separated):")
        elif "car" in message:
            route_parsing = 3
            updateJsonData(fname, route_parsing, location, "car", destinations)
            return respond("List the locations you want to visit today (comma separated):")
        elif "transit" in message:
            route_parsing = 3
            updateJsonData(fname, route_parsing, location, "transit", destinations)
            return respond("List the locations you want to visit today (comma separated):")
        else:
            return respond("Invalid! Please enter one of the following\n" \
                           "'car', 'walk', 'cycle', 'transit'\n"
                           "or type 'cancel' to cancel input")
    elif route_parsing == 3:
        if message:
            places = message.split(",")
            for place in places:
                destinations.append(place.strip() + "," + location)
            route_parsing = 4
            updateJsonData(fname, route_parsing, location, transport, destinations)
            return respond("Here are the locations in optimal route order:\n" + route.route_reply_msg(destinations) + "\n" + "Do you want image guides? (yes, no)")
        else:
            return respond("Please input destinations, or type 'cancel' to escape")
    elif route_parsing == 4:
        route_parsing = 0
        updateJsonData(fname, route_parsing, location, transport, destinations)
        if "yes" in message:
            IMG_URL = staticmap.reply_image_msg(destinations, transport)
            response = MessagingResponse()
            msg = response.message("Enjoy your trip!")
            msg.media(IMG_URL)
            return str(response)
        else:
            return respond("Enjoy your trip!")
    elif 'dawae' in message:
        print('dawae')
        keywords = message.replace('dawae ', '')
        if keywords == '':
            return respond('No search term given. Please try again with keywords.')
        else:
            info = "What country are the locations in?"
            route_parsing = 1
            updateJsonData(fname, route_parsing, location, transport, destinations)
            return respond(info)
    elif "suggestions" in message:
        print("suggestions")
        keywords = message.replace('suggestions ', "")
        info = SerpApiSearches.search_location(keywords)

        return respond(info)
    elif 'help' in message or 'instruction' in message or 'how to' in message:
        print('help')
        return respond(HELP_STR1)
    else:
        return respond(HELP_STR2)

def updateJsonData(fname, route_parsing, location, transport, destinations):
    defaultData = {
        "route_parsing": route_parsing,
        "location": location,
        "transport": transport,
        "destinations": destinations
    }

    with open(fname, 'w') as outfile:
        json.dump(defaultData, outfile)