import os
import threading
from flask import Flask
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

# --- FLASK FOR RENDER LIVE ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "BOT LIVE - 500 Members Bot Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# --- DATABASE ---
conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS owners (channel_id TEXT PRIMARY KEY, owner_id TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, points INTEGER DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS promo (channel_link TEXT PRIMARY KEY, owner_id TEXT)")
conn.commit()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur.execute("INSERT OR IGNORE INTO users VALUES (?, 0)", (user_id,))
    conn.commit()
    cur.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    points = cur.fetchone()[0]
    
    await update.message.reply_text(
        f"🔥 **FREE 500 MEMBERS BOT** ❤️\n\n"
        f"Tumhare Points: {points}\n\n"
        f"**NOTE:** Pehle is bot ko @free_auto_earn_500_members_bot ko apne channel me Admin banao!\n\n"
        f"Commands:\n"
        f"/add @channel ya link - Channel add karo\n"
        f"/earn - Points kamao\n"
        f"/bonus - First time 10 free points lo\n"
        f"/my_channels - Tumhare channels"
    )

# --- BONUS COMMAND (Tumhare liye fix) ---
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur.execute("INSERT OR IGNORE INTO users VALUES (?, 0)", (user_id,))
    cur.execute("UPDATE users SET points = points + 10 WHERE user_id=?", (user_id,))
    conn.commit()
    await update.message.reply_text("✅ 10 Points mil gaye! Ab /add https://t.me/+Ft2l_-QwyA03OGNl karo")

# --- /earn ---
async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur.execute("SELECT * FROM promo WHERE owner_id != ?", (user_id,))
    rows = cur.fetchall()
    if not rows:
        await update.message.reply_text("Abhi koi channel nahi hai join karne ko. Thodi der baad aao!\n\nLekin tum /bonus se 10 points le sakte ho!")
        return
    
    text = "Join karo points ke liye:\n\n"
    for r in rows[:5]:
        text += f"{r[0]}\n"
    text += "\nJoin karke /verify likho"
    await update.message.reply_text(text)

# --- /add ---
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    points = row[0] if row else 0

    if points < 1:
        await update.message.reply_text(f"Points kam hain! {points} hai, 1 chahiye. /earn ya /bonus se kamao")
        return

    if not context.args:
        await update.message.reply_text("Example: /add @my_love_channel ya /add https://t.me/+Ft2l_-QwyA03OGNl")
        return

    link = context.args[0]
    # Private link ko bhi allow karo
    cur.execute("INSERT OR REPLACE INTO promo VALUES (?, ?)", (link, user_id))
    cur.execute("UPDATE users SET points = points - 1 WHERE user_id=?", (user_id,))
    conn.commit()
    await update.message.reply_text(f"✅ Channel Added! {link}\n\nAb ispe members aayenge. 1 Point kata hai.")

async def my_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur.execute("SELECT channel_link FROM promo WHERE owner_id=?", (user_id,))
    rows = cur.fetchall()
    if not rows:
        await update.message.reply_text("Tumne abhi koi channel add nahi kiya.")
    else:
        txt = "Tumhare Channels:\n" + "\n".join([r[0] for r in rows])
        await update.message.reply_text(txt)

# --- AUTO OWNER WHEN ADMIN ---
async def handle_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member:
        chat = update.my_chat_member.chat
        new_status = update.my_chat_member.new_chat_member.status
        old_status = update.my_chat_member.old_chat_member.status
        
        if new_status in ["administrator"] and old_status in ["left", "kicked", "member"]:
            if chat.type == "channel":
                owner_id = str(update.my_chat_member.from_user.id)
                channel_id = str(chat.id)
                cur.execute("INSERT OR REPLACE INTO owners VALUES (?, ?)", (channel_id, owner_id))
                conn.commit()
                try:
                    await context.bot.send_message(
                        chat_id=owner_id,
                        text=f"🔥 Congrats! Tum {chat.title} ({channel_id}) ke OWNER ban gaye!"
                    )
                except:
                    pass

# --- MAIN ---
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    
    if not BOT_TOKEN:
        print("BOT_TOKEN nahi mila!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bonus", bonus))
    app.add_handler(CommandHandler("earn", earn))
    app.add_handler(CommandHandler("add", add_channel))
    app.add_handler(CommandHandler("my_channels", my_channels))
    app.add_handler(ChatMemberHandler(handle_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    
    print("BOT LIVE - 500 Members Bot Started")
    app.run_polling()

if __name__ == "__main__":
    main()
