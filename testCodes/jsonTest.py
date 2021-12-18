import json


defaultData = {
  "route_parsing": 3,
  "location": "",
  "transport": "walk",
  "destinations": []
}

with open('../data.json', 'w') as outfile:
    json.dump(defaultData, outfile)

with open("../data.json") as json_file:
    data = json.load(json_file)
    print(data)
    route_parsing = data["route_parsing"]
    location = data["location"]
    transport = data["transport"]
    destinations = data["destinations"]

    print(route_parsing)