import requests
import json
import re

def request_to_api(url:str, headers:dict, querystring:dict) -> json:
    '''
    Функиця для запросов к базы данных

    :param url: адрес поиска
    :param headers: запрос
    :param querystring: словарь с хостом и ключом
    :return: информация из базы данных
    '''
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except Exception:
        print('Что-то пошло не так.')

def caption_id(data:str, quantity:int = 8) -> list or None:
    '''
    Функция для получения информации с названиями районов и их ид из базы данных

    :param data: город поиска
    :param quantity: количество вариантов
    :return: список с названиями и ид
    '''
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

    for i, val in enumerate(find1):
        result.append([val, find[i + len(find1)]])

    if result:
        return result

    return None