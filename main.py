import os, threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask - 24/7 Live ke liye
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Live 24/7 - 5 Channels"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- TERE 5 CHANNELS ---
CHANNELS = [
    {"name": "Channel 1", "link": "https://t.me/+j88DIVGmn2E5NzU1"},
    {"name": "Channel 2", "link": "https://t.me/+xJMM2UHedVhjMGI9"},
    {"name": "Channel 3", "link": "https://t.me/+vRvc1P5mRqsxZTU9"},
    {"name": "Channel 4", "link": "https://t.me/+6UDI9GKqHEphNDk9"},
    {"name": "Channel 5", "link": "https://t.me/+bXf7mF-0Lh04YTY9"},
]

VERIFY_CHANNEL = "https://t.me/+d7y1Wl2qRGphMTg1"

def make_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 Channel 1", url=CHANNELS[0]["link"]),
         InlineKeyboardButton("🔴 Channel 2", url=CHANNELS[1]["link"])],
        [InlineKeyboardButton("🔴 Channel 3", url=CHANNELS[2]["link"]),
         InlineKeyboardButton("🔴 Channel 4", url=CHANNELS[3]["link"])],
        [InlineKeyboardButton("🔴 Channel 5", url=CHANNELS[4]["link"])],
        [InlineKeyboardButton("✅ VERIFY JOINED", callback_data="verify")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""💎✨ WELCOME, {update.effective_user.first_name} ✨💎

🔥 WELCOME TO DRIP CLIENT 🔥
___________________________
🔐 JOIN ALL 5 CHANNELS TO CONTINUE

Join All 5 Channel Mod Apk Links 🔗❤
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

def main
