from loader import bot
from telebot.types import Message
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import json
import re

def area_markup(areas):
    destinations = InlineKeyboardMarkup()

    for area in areas:
        destinations.add(InlineKeyboardButton(text=area[0],
                          callback_data='ar'+area[1]))
    return destinations
