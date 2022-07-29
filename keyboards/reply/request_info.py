import requests
import json
import re

def request_to_api(url, headers, querystring):
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except Exception:
        print('Что-то пошло не так.')

def caption_and_id_receiving(data:str, quantity:int = 8):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": "{}".format(data), "locale": "en_US"}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57" }
    text = json.dumps(request_to_api(url, headers, querystring))

    pattern1 = r'(?<="caption": ")[^"]+'
    find1 = re.findall(pattern1, text)

    pattern2 = r'(?<="destinationId": ")[^"]+'
    find2 = re.findall(pattern2, text)

    if quantity > 10:
        quantity = 10
    elif quantity < 1:
        quantity = 1

    find1 = find1[0:quantity]
    i_number = 0
    for i in find1:
        if 'span' in i:
            pattern = r'(<span.+span>)'
            find = re.split(pattern, i)
            find1[i_number] = find[0] + find[2]
        i_number += 1
    find2 = find2[0:quantity]
    find = find1 + find2
    result = []

    for i in range(len(find1)):
        result.append([find[i], find[i + len(find1)]])

    return result

def price_and_distance_receiving(text:str):
    pattern1 = r'(?<="label": ")[^"]+'
    find1 = re.findall(pattern1, text)

    pattern2 = r'(?<="distance": ")[^( miles")]+'
    find2 = re.findall(pattern2, text)

    pattern3 = r'(?<="id": )[^,]+'
    find3 = re.findall(pattern3, text)

    pattern4 = r'(?<="current": ")[^"]+'
    find4 = re.findall(pattern4, text)

    mainlabel = find1[0]
    newfind1 = []
    newfind2 = []
    newfind3 = []
    index = 0
    for i in find1:
        if i == mainlabel:
            newfind1.append(find2[index])
            newfind2.append(find3[index + 1])
            newfind3.append(find4[index])
        index += 1
        if index > 30:
            break

    return mainlabel, newfind1, newfind2, newfind3