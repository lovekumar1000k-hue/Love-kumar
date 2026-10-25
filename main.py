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

# 5 SLOTS
SLOT1 = "https://t.me/+j88DIVGmn2E5NzU1"
SLOT2 = "https://t.me/+xJMM2UHedVhjMGI9"
SLOT3 = "https://t.me/+vRvc1P5mRqsxZTU9"
SLOT4 = "https://t.me/+6UDI9GKqHEphNDk9"
SLOT5 = "https://t.me/+bXf7mF-0Lh04YTY9"

# VERIFY CHANNEL
VERIFY = "https://t.me/+d7y1Wl2qRGphMTg1"

def make_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 SLOT 1 - Join", url=SLOT1)],
        [InlineKeyboardButton("🔴 SLOT 2 - Join", url=SLOT2)],
        [InlineKeyboardButton("🔴 SLOT 3 - Join", url=SLOT3)],
        [InlineKeyboardButton("🔴 SLOT 4 - Join", url=SLOT4)],
        [InlineKeyboardButton("🔴 SLOT 5 - Join", url=SLOT5)],
        [InlineKeyboardButton("✅ VERIFY JOINED", callback_data="verify")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""💎 WELCOME {update.effective_user.first_name} 💎

🔥 WELCOME TO DRIP CLIENT 🔥
___________________________
🔐 JOIN ALL 5 SLOTS TO CONTINUE

5 Slot Join Karo - Mod Link Ke Liye
___________________________
"""
    await update.message.reply_text(text, reply_markup=make_keyboard())

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "✅ Verified! Niche se Key le lo 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔑 VERIFY GET KEY", url=VERIFY)]
        ])
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ID: {update.effective_chat.id}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
    print("Bot Started - 5 Slot + Verify")
    app.run_polling()

if __name__ == "__main__":
    main()
