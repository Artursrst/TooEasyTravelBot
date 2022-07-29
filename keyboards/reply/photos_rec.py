from keyboards.reply.request_info import request_to_api

def photos_receiving(data:int, quantity:int = 0) -> list or None:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": "{}".format(data)}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    rec = request_to_api(url, headers, querystring)
    if quantity > 4:
        quantity = 4
    elif quantity <= 0:
        return None
    result = []

    for i in range(quantity):
        result.append(rec['hotelImages'][i]['baseUrl'].format(size = rec['hotelImages'][i]['sizes'][0]['suffix']))

    return result