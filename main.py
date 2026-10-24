import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "TRANSFER Bot ON hai ✅\n\n"
        "Bot ke DM me: /add <channel_link>\n"
        "Group me: Kisi ke msg pe reply karke /setowner"
    )

# /add command (DM wala)
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /add https://t.me/+Ft2l_-QwyA03OGNl")
        return
    link = context.args[0]
    # yahan tera 11 channel wala logic tha, wo yahan rahega
    # demo ke liye:
    await update.message.reply_text(f"Channel Add ho gaya: {link} ✅\nAb /earn se members ayenge.")

# /setowner command (Group wala - TRANSFER jaisa)
async def setowner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Group me hi kaam karega
    if update.effective_chat.type == 'private':
        await update.message.reply_text("❌ Ye command DM me nahi, Group me use karo!\nGroup me kisi ke msg pe reply karke /setowner likho")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe REPLY karke /setowner likho")
        return

    try:
        user = update.message.reply_to_message.from_user
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            can_change_info=True
        )
        await context.bot.set_chat_administrator_custom_title(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            custom_title="Owner ❤️"
        )
        await update.message.reply_text(f"Done! {user.first_name} ko Owner ❤️ bana diya (prank wala)")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}\nBot ko Admin banao aur 'Add new admins' ON karo")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_channel))
    app.add_handler(CommandHandler("setowner", setowner))
    app.run_polling()

if __name__ == "__main__":
    main()
