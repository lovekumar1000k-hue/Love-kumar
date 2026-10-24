import os, threading, sqlite3
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Render pe DB ke liye
DB_FILE = "members.db"

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "500 MEMBERS BOT LIVE"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# ---- DATABASE ----
def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, owner_id INTEGER, joins INTEGER DEFAULT 0)")
    con.commit(); con.close()

def get_user(user_id):
    con = sqlite3.connect(DB_FILE); cur = con.cursor()
    cur.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO users VALUES (?, 0)", (user_id,)); con.commit(); row = (0,)
    con.close(); return row[0]

def add_points(user_id, pts):
    con = sqlite3.connect(DB_FILE); cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO users VALUES (?, 0)", (user_id,))
    cur.execute("UPDATE users SET points = points + ? WHERE user_id=?", (pts, user_id))
    con.commit(); con.close()

# ---- BOT LOGIC ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = get_user(user_id)
    text = f"👋 FREE 500 MEMBERS BOT\n\n💰 Tumhare Points: {points}\n\n🔥 Channel kaise badhaye?\n1. /earn - Channel join karke point kamao\n2. /add @yourchannel - Apna channel add karo (1 point = 1 member)\n\nBot ko apne channel me Admin banao tabhi add hoga!"
    buttons = [[InlineKeyboardButton("💸 Earn Points", callback_data="earn")],
               [InlineKeyboardButton("➕ Add Channel", callback_data="howtoadd")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    con = sqlite3.connect(DB_FILE); cur = con.cursor()
    cur.execute("SELECT username FROM channels LIMIT 5")
    rows = cur.fetchall(); con.close()
    if not rows:
        await update.message.reply_text("Abhi koi channel nahi hai join karne ko. Thodi der baad aao!")
        return
    for (ch_username,) in rows:
        # check if already joined
        try:
            member = await context.bot.get_chat_member(chat_id=f"@{ch_username}", user_id=update.effective_user.id)
            if member.status in ['member','administrator','creator']:
                continue
        except: pass
        
        btn = [[InlineKeyboardButton(f"Join @{ch_username}", url=f"https://t.me/{ch_username}")],
               [InlineKeyboardButton("✅ Joined - Check", callback_data=f"check_{ch_username}")]]
        await update.message.reply_text(f"👉 Join karo @{ch_username} aur 1 point pao!", reply_markup=InlineKeyboardMarkup(btn))
        return
    await update.message.reply_text("Sab channels join kar liye! /start likho")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "earn":
        await earn(query, context)
    elif data == "howtoadd":
        await query.message.reply_text("Apna channel add karne ke liye:\n\n`/add @yourchannel_username`\n\nExample: `/add @my_love_channel`\n\n**Note:** Pehle is bot ko @free_auto_earn_500_members_bot ko apne channel me Admin banao!")
    elif data.startswith("check_"):
        ch_username = data.split("check_")[1]
        try:
            member = await context.bot.get_chat_member(chat_id=f"@{ch_username}", user_id=user_id)
            if member.status in ['member','administrator','creator']:
                add_points(user_id, 1)
                # increase join count and remove if target reached (optional)
                con = sqlite3.connect(DB_FILE); cur = con.cursor()
                cur.execute("UPDATE channels SET joins = joins + 1 WHERE username=?", (ch_username,))
                con.commit(); con.close()
                await query.message.reply_text(f"✅ Verified! @{ch_username} join kar liya. +1 Point mila! Total: {get_user(user_id)}")
            else:
                await query.message.reply_text(f"❌ Abhi join nahi kiya! Pehle @{ch_username} join karo fir Check dabao.")
        except Exception as e:
            await query.message.reply_text(f"Error: Bot us channel ka admin nahi hai @{ch_username}")

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Use: /add @yourchannel\nExample: /add @my_channel")
        return
    ch = context.args[0].replace("@","").replace("https://t.me/","")
    user_id = update.effective_user.id
    points = get_user(user_id)
    if points < 1:
        await update.message.reply_text(f"Points kam hain! {points} hai, 1 chahiye. /earn se kamao")
        return
    # check bot is admin in that channel
    try:
        me = await context.bot.get_chat_member(chat_id=f"@{ch}", user_id=context.bot.id)
        if me.status not in ['administrator','creator']:
            await update.message.reply_text(f"❌ Pehle mujhe @{ch} me Admin banao!")
            return
    except:
        await update.message.reply_text(f"❌ Mujhe @{ch} me Admin banao aur channel public rakho!")
        return

    con = sqlite3.connect(DB_FILE); cur = con.cursor()
    cur.execute("INSERT INTO channels (username, owner_id) VALUES (?, ?)", (ch, user_id))
    cur.execute("UPDATE users SET points = points - 1 WHERE user_id=?", (user_id,))
    con.commit(); con.close()
    await update.message.reply_text(f"✅ Channel @{ch} add ho gaya! Ab log usko join karenge. 1 point kata. Bache: {points-1}")

def main():
    init_db()
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("earn", earn))
    app.add_handler(CommandHandler("add", add_channel))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("500 Members Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
