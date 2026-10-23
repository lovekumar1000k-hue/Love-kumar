import os
from telebot import TeleBot, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

LINK1 = "https://t.me/+LqVblnrPGUgyMDZl"
LINK2 = "https://t.me/+yoY115wHhqVmODhl"
LINK3 = "https://t.me/+oYGxMsFWzrpjYjU1"
LINK4 = "https://t.me/+OD25svaX8vYyZDg1"
LINK5 = "https://t.me/+Ft2l_-QwyA03OGNl"
PANEL_LINK = "https://t.me/+LqVblnrPGUgyMDZl"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Join Channel 1 🔥", url=LINK1))
    markup.add(types.InlineKeyboardButton("Join Channel 2 🔥", url=LINK2))
    markup.add(types.InlineKeyboardButton("Join Channel 3 🔥", url=LINK3))
    markup.add(types.InlineKeyboardButton("Join Channel 4 🔥", url=LINK4))
    markup.add(types.InlineKeyboardButton("Join Channel 5 🔥", url=LINK5))
    markup.add(types.InlineKeyboardButton("✅ I Joined - Get Panel", callback_data="joined"))
    bot.send_message(message.chat.id, "🔥 Panel lene ke liye 5 Channel Join karo 👇\nSab par alag link hai!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == "joined":
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("GET PANEL OR KEY 🔑", url=PANEL_LINK))
        markup2.add(types.InlineKeyboardButton("GET KEY 🔑", url=PANEL_LINK))
        bot.send_message(call.message.chat.id, "✅ Thanks for joining!\nNeeche se Panel / Key le lo 👇", reply_markup=markup2)

bot.infinity_polling()
