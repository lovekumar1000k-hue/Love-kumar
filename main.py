import telebot
from telebot import types

BOT_TOKEN = "8346793148:AAE1UTWzP0KUc3l4nbNvmtIHGVt-GoaTyyc"
INVITE_LINK = "https://t.me/+LqVblnrPGUgyMDZl"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Join Channel 1 🔥", url=INVITE_LINK))
    markup.add(types.InlineKeyboardButton("Join Channel 2 🔥", url=INVITE_LINK))
    markup.add(types.InlineKeyboardButton("Join Channel 3 🔥", url=INVITE_LINK))
    markup.add(types.InlineKeyboardButton("Join Channel 4 🔥", url=INVITE_LINK))
    markup.add(types.InlineKeyboardButton("Join Channel 5 🔥", url=INVITE_LINK))
    markup.add(types.InlineKeyboardButton("✅ I Joined - Get Panel", callback_data="check"))
    bot.send_message(message.chat.id, "Panel lene ke liye 5 baar join karo 👇\n\nSame link hai, 5 baar click karke join ho jao", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def check(call):
    try:
        with open('panel.jpg','rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption="🔥 FREE FIRE NON-ROOT ANTIBAN PANEL 🔥\n\nBR-CS-CUSTOM WORKING 100%")
    except:
        bot.send_message(call.message.chat.id, "panel.jpg upload nahi hua! Github me panel.jpg naam se photo upload karo")

bot.infinity_polling()
