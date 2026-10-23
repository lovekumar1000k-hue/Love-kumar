import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    {"name": "Channel 1", "link": "https://t.me/+j88DIVGmn2E5NzU1", "id": -1002749876541},
    {"name": "Channel 2", "link": "https://t.me/+Z6d9MP1fJDZkYmQ1", "id": -1002749876542},
    {"name": "Channel 3", "link": "https://t.me/+HRybxM6SFVZjNzg0", "id": -1002749876543},
    {"name": "Channel 4", "link": "https://t.me/+_M8cMRaOYrlmZWE9", "id": -1002749876544},
    {"name": "Channel 5", "link": "https://t.me/+swQYM_Z0krdkYjM1", "id": -1002749876545},
]
VERIFY_CHANNEL = "https://t.me/+LqVblnrPGUgyMDZl"

async def check_status(bot, user_id):
    s = {}
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(ch["id"], user_id)
            s[ch["name"]] = m.status not in ['left','kicked']
        except:
            s[ch["name"]] = False
    return s

def make_keyboard(status=None):
    def dot(n):
        if not status: return "🔴"
        return "🟢" if status.get(n) else "🔴"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{dot('Channel 1')} Channel 1", url=CHANNELS[0]["link"]),
         InlineKeyboardButton(f"{dot('Channel 2')} Channel 2", url=CHANNELS[1]["link"])],
        [InlineKeyboardButton(f"{dot('Channel 3')} Channel 3", url=CHANNELS[2]["link"]),
         InlineKeyboardButton(f"{dot('Channel 4')} Channel 4", url=CHANNELS[3]["link"])],
        [InlineKeyboardButton(f"{dot('Channel 5')} Channel 5", url=CHANNELS[4]["link"])],
        [InlineKeyboardButton("✅ VERIFY JOINED", callback_data="verify")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""💎✨ WELCOME, {update.effective_user.first_name} ✨💎

🔥 WELCOME TO DRIP CLIENT 🔥
___________________________

🔐 JOIN ALL CHANNELS TO CONTINUE

🔴 1. Tap all channel buttons
🟢 2. Join each channel
🔴 3. Press VERIFY JOINED
🟢 4. Continue after verification

Join All Channel Mod Apk Links 🔗❤
___________________________

⚡ FAST • SECURE • FREE ⚡
"""
    await update.message.reply_text(text, reply_markup=make_keyboard())

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    status = await check_status(context.bot, q.from_user.id)
    not_joined = [k for k,v in status.items() if not v]
    if not_joined:
        await q.edit_message_reply_markup(reply_markup=make_keyboard(status))
        await q.message.reply_text(f"❌ Baki hai: {', '.join(not_joined)}")
    else:
        await q.message.reply_text("✅ Done!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 VERIFY GET KEY", url=VERIFY_CHANNEL)]]))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    app.run_polling()

if __name__ == "__main__":
    main()
