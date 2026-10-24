import os, threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask - 24/7 Live ke liye
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Live 24/7 - 11 Channels"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- TERE 11 CHANNELS ---
CHANNELS = [
    {"name": "Channel 1", "link": "https://t.me/+j88DIVGmn2E5NzU1"},
    {"name": "Channel 2", "link": "https://t.me/+mnPocSRmQlwyMmJl"},
    {"name": "Channel 3", "link": "https://t.me/+6UDI9GKqHEphNDk9"},
    {"name": "Channel 4", "link": "https://t.me/+Z6d9MP1fJDZkYmQ1"},
    {"name": "Channel 5", "link": "https://t.me/+ADDtPC_lBFNmY2U1"},
    {"name": "Channel 6", "link": "https://t.me/+swQYM_Z0krdkYjM1"},
    {"name": "Channel 7", "link": "https://t.me/+_M8cMRaOYrlmZWE9"},
    {"name": "Channel 8", "link": "https://t.me/+xJMM2UHedVhjMGI9"},
    {"name": "Channel 9", "link": "https://t.me/+vRvc1P5mRqsxZTU9"},
    {"name": "Channel 10", "link": "https://t.me/+HRybxM6SFVZjNzg0"},
    {"name": "Channel 11", "link": "https://t.me/+bXf7mF-0Lh04YTY9"},
]

VERIFY_CHANNEL = "https://t.me/+d7y1Wl2qRGphMTg1"

def make_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 Channel 1", url=CHANNELS[0]["link"]),
         InlineKeyboardButton("🔴 Channel 2", url=CHANNELS[1]["link"])],
        [InlineKeyboardButton("🔴 Channel 3", url=CHANNELS[2]["link"]),
         InlineKeyboardButton("🔴 Channel 4", url=CHANNELS[3]["link"])],
        [InlineKeyboardButton("🔴 Channel 5", url=CHANNELS[4]["link"]),
         InlineKeyboardButton("🔴 Channel 6", url=CHANNELS[5]["link"])],
        [InlineKeyboardButton("🔴 Channel 7", url=CHANNELS[6]["link"]),
         InlineKeyboardButton("🔴 Channel 8", url=CHANNELS[7]["link"])],
        [InlineKeyboardButton("🔴 Channel 9", url=CHANNELS[8]["link"]),
         InlineKeyboardButton("🔴 Channel 10", url=CHANNELS[9]["link"])],
        [InlineKeyboardButton("🔴 Channel 11", url=CHANNELS[10]["link"])],
        [InlineKeyboardButton("✅ VERIFY JOINED", callback_data="verify")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""💎✨ WELCOME, {update.effective_user.first_name} ✨💎

🔥 WELCOME TO DRIP CLIENT 🔥
___________________________
🔐 JOIN ALL 11 CHANNELS TO CONTINUE

Join All 11 Channel Mod Apk Links 🔗❤
___________________________
⚡ FAST • SECURE • FREE ⚡"""
    await update.message.reply_text(text, reply_markup=make_keyboard())

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "✅ Verified! Ab Key Lo 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔑 VERIFY GET KEY", url=VERIFY_CHANNEL)]
        ])
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ID: `{update.effective_chat.id}`", parse_mode="Markdown")

def main():
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    print("Bot Started with 11 Channels...")
    app.run_polling()

if __name__ == "__main__":
    main()
