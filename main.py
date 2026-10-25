# --- FIX FOR PYTHON 3.14 ON RENDER ---
import sys, types
if 'imghdr' not in sys.modules:
    m = types.ModuleType('imghdr')
    def what(file, h=None): return None
    m.what = what
    sys.modules['imghdr'] = m
# --- FIX END ---

import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot Live 24/7 - 5 Slot + Verify"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

SLOT1 = "https://t.me/+j88DIVGmn2E5NzU1"
SLOT2 = "https://t.me/+xJMM2UHedVhjMGI9"
SLOT3 = "https://t.me/+vRvc1P5mRqsxZTU9"
SLOT4 = "https://t.me/+6UDI9GKqHEphNDk9"
SLOT5 = "https://t.me/+bXf7mF-0Lh04YTY9"
VERIFY = "https://t.me/+d7y1Wl2qRGphMTg1"

def make_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 SLOT 1 - Join", url=SLOT1)],
        [InlineKeyboardButton("🔴 SLOT 2 - Join", url=SLOT2)],
        [InlineKeyboardButton
