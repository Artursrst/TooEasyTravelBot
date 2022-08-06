from urllib.request import urlopen

'''url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

querystring = {"id":"454786"}

headers = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
}


url = "https://hotels4.p.rapidapi.com/locations/v2/search"
querystring = {"query": "houston", "locale": "en_US"}
headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }

url = "https://hotels4.p.rapidapi.com/properties/list"
querystring = {"destinationId": "1410382"}
headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }

photos_receiving('2666535360', 4)'''

url = ('https://exp.cdn-hotels.com/hotels/33000000/32420000/32411000/32410977/708d7986_z.jpg')

image = urlopen(url)

