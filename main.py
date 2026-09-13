import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("8827274778:AAEWpWMAL6D5R26JUxcmtl_AxD2ehm2VH_0")

LINKS = [
    ("Channel 1", "https://t.me/+kgcuP0beVJFlMTBl"),
    ("Channel 2", "https://t.me/+TsnRewwQjtgyMWI1"),
    ("Channel 3", "https://t.me/+qaju-Z1MpUMyYTBl"),
    ("Channel 4", "https://t.me/+PmNlaBj7WCk4ZjY1"),
    ("Channel 5", "https://t.me/+LgxFzjXBp840MGVl"),
    ("Channel 6", "https://t.me/+UhajwZ_6h_kwYmJl"),
    ("Channel 7", "https://t.me/+q0RvCoA_Vic4ZTc1"),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = []
    for i in range(0, len(LINKS), 2):
        kb.append([InlineKeyboardButton(t, url=u) for t, u in LINKS[i:i+2]])
    await update.message.reply_text("🔐 P2077 KING BOT\n\nSab join karo 👇", reply_markup=InlineKeyboardMarkup(kb))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
