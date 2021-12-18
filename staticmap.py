import secrets
import requests
import base64
import route


def reply_image_msg(arr):
    route_info = route.get_address_json(arr)
    markers_output_str = ''
    for r in route_info:
        lat, long = (r['lat'], r['lng'])
        temp_str = f"&markers={lat}%2C{long}"
        markers_output_str += temp_str

    # print(markers_output_str)

    response = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=800x500&{markers_output_str}"
                            f"&key={secrets.maps_api}")

    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": secrets.imgbb_api,
        "image": base64.b64encode(response.content),
    }
    res = requests.post(url, payload)

    if res.status_code == 200:
        json = res.json()
        print(json['data']['url'])
        return json['data']['url']

    else:
        return None

