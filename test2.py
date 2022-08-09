import json
from utils.misc.request_info import request_to_api
import requests

'''url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

querystring = {"id":"454786"}

headers = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
}'''


'''url = "https://hotels4.p.rapidapi.com/locations/v2/search"
querystring = {"query": "houston", "locale": "en_US"}
headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }'''



'''url = "https://hotels4.p.rapidapi.com/properties/list"
querystring = {"destinationId": "1410382"}
headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }'''

url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query":"new york","locale":"en_US","currency":"USD"}

headers = {
	"X-RapidAPI-Key": "3a79ba62e0msh37989a720c1c081p108357jsnbf5d74c17a9a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

'''with open('city.json', 'w') as file:
    json.dump(request_to_api(url, headers, querystring), file, indent=4)'''

with open('city3.json', 'w') as file:
	response = requests.request("GET", url, headers=headers, params=querystring)
	json.dump(json.loads(response.text), file, indent=4)



