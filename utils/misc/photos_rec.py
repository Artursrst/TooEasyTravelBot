from utils.misc.request_info import request_to_api
import json

def photos_receiving(data:int, quantity:int = 0) -> list or None:
    '''
    Функция для получения фотографий из базы данных

    :param data: ид отеля
    :param quantity: количество фотографий
    :return: список с ссылками на фотографии
    '''
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": "{}".format(data)}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    with open('photos.json', 'w') as file:
        json.dump(request_to_api(url, headers, querystring), file, indent=4)
    rec = request_to_api(url, headers, querystring)
    if quantity > 4:
        quantity = 4
    elif quantity <= 0:
        return None
    result = []

    for i in range(quantity):
        result.append(rec['hotelImages'][i]['baseUrl'].format(size = rec['hotelImages'][i]['sizes'][0]['suffix']))

    return result