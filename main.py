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
    return "BOT LIVE - Owner Bot Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# --- DATABASE ---
conn = sqlite3.connect("owners.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS channels (channel_id TEXT PRIMARY KEY, owner_id TEXT)")
conn.commit()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# --- /start COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Live hai!\n\n"
        "Mujhe apne Channel me Admin banao, tum automatic Owner ban jaoge.\n\n"
        "Command:\n"
        "/my_channels - Tumhare channels dekho"
    )

async def my_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    cur = conn.cursor()
    cur.execute("SELECT channel_id FROM channels WHERE owner_id=?", (user_id,))
    rows = cur.fetchall()
    if not rows:
        await update.message.reply_text("Tum abhi kisi channel ke owner nahi ho.")
    else:
        txt = "Tumhare Channels:\n" + "\n".join([r[0] for r in rows])
        await update.message.reply_text(txt)

# --- JAB CHANNEL ME ADMIN BANAYE ---
async def handle_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Jab bot ko kisi channel/group me add kiya jaye
    if update.my_chat_member:
        chat = update.my_chat_member.chat
        new_status = update.my_chat_member.new_chat_member.status
        old_status = update.my_chat_member.old_chat_member.status
        
        # Agar bot ko admin banaya gaya
        if new_status in ["administrator", "member"] and old_status in ["left", "kicked", "member"]:
            if chat.type == "channel":
                owner_id = str(update.my_chat_member.from_user.id)
                channel_id = str(chat.id)
                
                # Save owner
                conn.execute("INSERT OR REPLACE INTO channels VALUES (?, ?)", (channel_id, owner_id))
                conn.commit()
                
                try:
                    await context.bot.send_message(
                        chat_id=owner_id,
                        text=f"🔥 Congrats! Tum {chat.title} ({channel_id}) ke OWNER ban gaye!\n\nAb is channel ka control tumhare paas hai."
                    )
                except:
                    pass

# --- MAIN ---
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    
    if not BOT_TOKEN:
        print("BOT_TOKEN nahi mila! Render Environment me daalo")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("my_channels", my_channels))
    app.add_handler(ChatMemberHandler(handle_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    
    print("BOT LIVE - Owner Bot Started
