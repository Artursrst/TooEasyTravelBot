import re
import json
from utils.misc.request_info import request_to_api

def get_mainlabel(data:str) -> str:
    '''
    Функция для поиска названия достопримечательности от которой происходит отсчёт расстояния до отеля

    :param data: id района
    :return: название достопримечательности
    '''
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": "{}".format(data)}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    text = json.dumps(request_to_api(url, headers, querystring))

    pattern1 = r'(?<="label": ")[^"]+'
    find1 = re.findall(pattern1, text)

    mainlabel = find1[0]

    return mainlabel