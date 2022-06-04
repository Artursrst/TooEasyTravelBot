from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()


'''
url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query":"new york"}

headers = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
}

response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId":"1635530"}

headers = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
}

response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)

with open('data2.json', 'w') as file:
    json.dump(data, file, indent=4)'''

'''bot = telebot.TeleBot('5377169411:AAEEIOPjuS7jdWBFVSJUpZ9HIF7nyjjiZ20');

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Hello World!")

bot.polling(none_stop=True, interval=0)'''



