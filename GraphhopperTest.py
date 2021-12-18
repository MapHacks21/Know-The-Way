import requests
import secrets

post_url = 'https://graphhopper.com/api/1/vrp/optimize?key=' + secrets.graphhopperKey
headers = {"Content-Type": "application/json"}
data = {
  "vehicles": [
    {
      "vehicle_id": "vehicle-1",
      "type_id": "cargo-bike",
      "start_address": {
        "location_id": "berlin",
        "lon": 13.406,
        "lat": 52.537
      },
      "earliest_start": 1554804329,
      "latest_end": 1554808329,
      "max_jobs": 3
    }
  ],
  "vehicle_types": [
    {
      "type_id": "cargo-bike",
      "capacity": [
        10
      ],
      "profile": "bike"
    }
  ],
  "services": [
    {
      "id": "s-1",
      "name": "visit-Joe",
      "address": {
        "location_id": "13.375854_52.537338",
        "lon": 13.375854,
        "lat": 52.537338
      },
      "size": [
        1
      ],
      "time_windows": [
        {
          "earliest": 1554805329,
          "latest": 1554806329
        }
      ]
    },
    {
      "id": "s-2",
      "name": "serve-Peter",
      "address": {
        "location_id": "13.393364_52.525851",
        "lon": 13.393364,
        "lat": 52.525851
      },
      "size": [
        1
      ]
    },
    {
      "id": "s-3",
      "name": "visit-Michael",
      "address": {
        "location_id": "13.416882_52.523543",
        "lon": 13.416882,
        "lat": 52.523543
      },
      "size": [
        1
      ]
    },
    {
      "id": "s-4",
      "name": "do nothing",
      "address": {
        "location_id": "13.395767_52.514038",
        "lon": 13.395767,
        "lat": 52.514038
      },
      "size": [
        1
      ]
    }
  ],
  "shipments": [
    {
      "id": "7fe77504-7df8-4497-843c-02d70b6490ce",
      "name": "pickup and deliver pizza to Peter",
      "priority": 1,
      "pickup": {
        "address": {
          "location_id": "13.387613_52.529961",
          "lon": 13.387613,
          "lat": 52.529961
        }
      },
      "delivery": {
        "address": {
          "location_id": "13.380575_52.513614",
          "lon": 13.380575,
          "lat": 52.513614
        }
      },
      "size": [
        1
      ],
      "required_skills": [
        "physical strength"
      ]
    }
  ],
  "objectives": [
    {
      "type": "min",
      "value": "vehicles"
    },
    {
      "type": "min",
      "value": "completion_time"
    }
  ],
  "configuration": {
    "routing": {
      "calc_points": True,
      "snap_preventions": [
        "motorway",
        "trunk",
        "tunnel",
        "bridge",
        "ferry"
      ]
    }
  }
}

res_jobid = requests.post(post_url, json=data, headers=headers)

print(res_jobid.text)
res_jobid_Json = res_jobid.json()

new_jobid = res_jobid_Json["job_id"]
print(new_jobid)

job_url = "https://graphhopper.com/api/1/vrp/solution/" + new_jobid + "?key=" + secrets.graphhopperKey
get_res = requests.get(job_url)

print(get_res.text)
print(get_res.json())

f = open("response.json", "w")
f.write(get_res.text)
f.close()


