
location1 = "afdasdfasdf1"
address1 = "afdasdfasdf1"
lat1, long1 = ("location1.latitude", "location1.longitude")

location2 = "afdasdfasdf2"
address2 = "afdasdfasdf2"
lat2, long2 = ("location2.latitude", "location2.longitude")

location3 = "afdasdfasdf3"
address3 = "afdasdfasdf3"
lat3, long3 = ("lat3", "location3.longitude")

dict1 = {"address":f"{address1}", "lat":f"{lat1}","lng":f"{long1}"}
dict2 = {"address":f"{address2}", "lat":f"{lat2}","lng":f"{long2}"}
dict3 = {"address":f"{address3}", "lat":f"{lat3}","lng":f"{long3}"}

arr = [dict1, dict2, dict3]

print(arr)