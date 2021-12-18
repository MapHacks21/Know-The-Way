from geopy.geocoders import Nominatim
import requests
import json
import secrets
import googlemaps
from datetime import datetime as dt

username = secrets.route_username
password = secrets.route_password
gmaps = googlemaps.Client(key=secrets.maps_api)

url = 'https://api.routexl.com/tour/'

geolocator = Nominatim(user_agent="knowtheway")


def get_address_json(arr):
    address_arr = []
    for location in arr:
        print(location)
        loc1 = geolocator.geocode(location)
        addr1 = loc1.address
        lat, long = (loc1.latitude, loc1.longitude)
        temp_dict = {"address": f"{addr1}", "lat": f"{lat}", "lng": f"{long}"}
        address_arr.append(temp_dict)

    return address_arr


def get_route(arr):
    address_arr = get_address_json(arr)
    print(address_arr)
    address_arr_json = json.dumps(address_arr)

    session = requests.Session()
    session.auth = (username, password)

    auth = session.post('https://' + 'api.routexl.com/tour/')

    realData = f"locations={address_arr_json}"
    response = session.post(url, data=realData)

    res_json = json.loads(response.content)

    return res_json['route']


def get_directions(start, end, transport):
    now = dt.now()
    directions_result = gmaps.directions(start,
                                         end,
                                         mode=transport,
                                         departure_time=now)

    results = directions_result[0]

    distance = results['legs'][0]['distance']['text']
    duration = results['legs'][0]['duration']['text']

    return [distance, duration]


def get_all_directions(info_json, transport):
    length = len(info_json)
    output = ''
    for i in range(0, length - 1):
        start = info_json[str(i)]['name']
        end = info_json[str(i + 1)]['name']
        temp_arr = get_directions(start, end, transport)

        start_str = start.split(',')[0]
        end_str = end.split(',')[0]

        temp_str = f"{i + 1}. {start_str} -> {end_str}\nThe distance is {temp_arr[0]}.\nThe duration is {temp_arr[1]}\n\n"
        output += temp_str

    return output


def route_reply_msg(arr, transport):
    route_info = get_route(arr)
    dir = get_all_directions(route_info, transport)

    return dir

# arr = ['nus, singapore', 'botanic gardens, singapore', 'vivo city, singapore']
# route_info = get_route(arr)
# t = 'transit'
# dir = get_all_directions(route_info, t)
#
# hi = get_directions('nus, singapore', 'vivo city, singapore', t)
#
# print(dir)

# geolocator = Nominatim(user_agent="knowtheway")
# location1 = geolocator.geocode("Sentosa, Singapore")
# address1 = location1.address
# lat1, long1 = (location1.latitude, location1.longitude)
#
# location2 = geolocator.geocode("NUS, Singapore")
# address2 = location2.address
# lat2, long2 = (location2.latitude, location2.longitude)
#
# location3 = geolocator.geocode("IKEA Alexandra, Singapore")
# address3 = location3.address
# lat3, long3 = (location3.latitude, location3.longitude)
#
# location4 = geolocator.geocode("Singapore Polytechnic, Singapore")
# address4 = location4.address
# lat4, long4 = (location4.latitude, location4.longitude)

# dict1 = {"address":f"{address1}", "lat":f"{lat1}","lng":f"{long1}"}
# dict2 = {"address":f"{address2}", "lat":f"{lat2}","lng":f"{long2}"}
# dict3 = {"address":f"{address3}", "lat":f"{lat3}","lng":f"{long3}"}
# dict4 = {"address":f"{address4}", "lat":f"{lat4}","lng":f"{long4}"}
#
# arr = [dict1, dict2, dict3, dict4]
#
# arrJson = json.dumps(arr)
#
# url = 'https://api.routexl.com/tour/'
#
# realData = f"locations={arrJson}"
#
# print(realData)

# d = 'locations=[{"address":"1","lat":"1.24894585","lng":"103.83430564159272"},{"address":"2","lat":"1.2962018",' \
#     '"lng":"103.77689943784759"},{"address":"3","lat":"1.288488","lng":"103.8059398"},{"address":"4","lat":"51.589548",' \
#     '"lng":"5.432482"}]'
#
# data = 'locations=[{"address":"1","lat":"52.05429","lng":"4.248618"},{"address":"2","lat":"52.076892",' \
#        '"lng":"4.26975"},{"address":"3","lat":"51.669946","lng":"5.61852"}]'
#
# session = requests.Session()
# session.auth = (username, password)
#
# auth = session.post('https://' + 'api.routexl.com/tour/')
# response = session.post(url,data=realData)
