from geopy.geocoders import Nominatim
import requests
import secrets

username = secrets.route_username
password = secrets.route_password

geolocator = Nominatim(user_agent="knowtheway")
location1 = geolocator.geocode("Sentosa, Singapore")
address1 = location1.address
lat1, long1 = (location1.latitude, location1.longitude)

location2 = geolocator.geocode("NUS, Singapore")
address2 = location2.address
lat2, long2 = (location2.latitude, location2.longitude)

location3 = geolocator.geocode("IKEA Alexandra, Singapore")
address3 = location3.address
lat3, long3 = (location3.latitude, location3.longitude)

dict1 = {"address":f"{address1}", "lat":f"{lat1}","lng":f"{long1}"}
dict2 = {"address":f"{address2}", "lat":f"{lat2}","lng":f"{long2}"}
dict3 = {"address":f"{address3}", "lat":f"{lat3}","lng":f"{long3}"}

arr = [dict1, dict2, dict3]

url = 'https://api.routexl.com/tour/'

realData = f"locations={arr}"

d = 'locations=[{"address":"1","lat":"1.24894585","lng":"103.83430564159272"},{"address":"2","lat":"1.2962018",' \
       '"lng":"103.77689943784759"},{"address":"3","lat":"1.288488","lng":"103.8059398"},{"address":"4","lat":"51.589548",' \
       '"lng":"5.432482"}]'

data = 'locations=[{"address":"1","lat":"52.05429","lng":"4.248618"},{"address":"2","lat":"52.076892",' \
       '"lng":"4.26975"},{"address":"3","lat":"51.669946","lng":"5.61852"}]'

session = requests.Session()
session.auth = (username, password)

auth = session.post('http://' + 'api.routexl.com/tour/')
response = session.post(url,data=d)

print(response.content)