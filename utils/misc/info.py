import json
import re
from utils.misc.request_info import request_to_api

def whole_info(data:str, q:int, h:str) -> list:
    '''
    Функция для получения основной информации из базы данных

    :param data: район поиска
    :param q: количество выводимых вариантов
    :param h: /highprice или /lowprice

    :return:
    :param mainlabel: достопримечательность для отсчёта расстояния
    :param rnewfind1: список расстояний до достопримечательности
    :param rnewfind2: список стоимостей за ночь
    :param rnewfind3: список адресов
    :param rnewfind4: список названий отелей
    :param rnewfind5: список ид отелей
    '''

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": "{}".format(data)}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    with open('holets.json', 'w') as file:
        json.dump(request_to_api(url, headers, querystring), file, indent=4)

    text = json.dumps(request_to_api(url, headers, querystring))

    pattern1 = r'(?<="label": ")[^"]+'
    find1 = re.findall(pattern1, text)

    pattern2 = r'(?<="distance": ")[^( miles")]+'
    find2 = re.findall(pattern2, text)

    pattern3 = r'(?<="current": ")[^"]+'
    find3 = re.findall(pattern3, text)

    pattern4 = r'(?<="streetAddress": ")[^"]+'
    find4 = re.findall(pattern4, text)

    pattern5 = r'(?<="name": ")[^"]+'
    find5 = re.findall(pattern5, text)

    pattern6 = r'(?<="id": )[^,]+'
    find6 = re.findall(pattern6, text)

    mainlabel = find1[0]
    newfind1 = []
    newfind2 = []
    newfind3 = []
    newfind4 = []
    newfind5 = []
    index = 0
    for i in find1:
        if i == mainlabel:
            newfind1.append(find2[index])
            newfind2.append(find3[index])
            newfind3.append(find4[index])
            newfind4.append(find5[index])
            newfind5.append(find6[index + 1])
        index += 1
        if index > 20:
            break
    doplist = []
    for i in newfind2:
        doplist.append(int(i[1:]))

    rnewfind1 = []
    rnewfind2 = []
    rnewfind3 = []
    rnewfind4 = []
    rnewfind5 = []

    if (len(newfind1) < q) or (len(newfind2) < q) or (len(newfind3) < q) or (len(newfind4) < q) or (len(newfind5) < q):
        q = min(len(newfind1), len(newfind2), len(newfind3), len(newfind4), len(newfind5))
    if h =='h':
        forsortlist = sorted(set(sorted(doplist, reverse=True)), reverse=True)
    else:
        forsortlist = sorted(set(sorted(doplist)))
    for i in forsortlist:
        index = 0
        for j in newfind2:
            if i == int(j[1:]):
                rnewfind1.append(newfind1[index])
                rnewfind2.append(newfind2[index])
                rnewfind3.append(newfind3[index])
                rnewfind4.append(newfind4[index])
                rnewfind5.append(newfind5[index])
            index += 1

    rnewfind1 = rnewfind1[:q]
    rnewfind2 = rnewfind2[:q]
    rnewfind3 = rnewfind3[:q]
    rnewfind4 = rnewfind4[:q]
    rnewfind5 = rnewfind5[:q]

    return mainlabel, rnewfind1, rnewfind2, rnewfind3, rnewfind4, rnewfind5