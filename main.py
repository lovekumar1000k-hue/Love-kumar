import os
from telebot import TeleBot, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set in Render!")

bot = TeleBot(BOT_TOKEN)

# Tere 5 alag links
LINK1 = "https://t.me/+LqVblnrPGUgyMDZl"
LINK2 = "https://t.me/+yoY115wHhqVmODhl"
LINK3 = "https://t.me/+oYGxMsFWzrpjYjU1"
LINK4 = "https://t.me/+OD25svaX8vYyZDg1"
LINK5 = "https://t.me/+Ft2l_-QwyA03OGNl"

PANEL_LINK = "https://t.me/+LqVblnrPGUgyMDZl"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Join Channel 1 🔥", url=
