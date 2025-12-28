from flask import Flask
from threading import Thread
import discord
import os

# --- KEEP ALIVE SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is awake!"
def run_web(): app.run(host='0.0.0.0', port=8080)

# --- BOT CONFIGURATION ---
TOKEN = 'YOUR_NEW_TOKEN_HERE' # Get a fresh one from Discord Portal!
MONITOR_CHANNEL_ID = 1289705151027875972  
SAVE_CHANNEL_ID = 1454783709298561085     
FILE_NAME = "Trade_Logs.txt"

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot Online: {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == MONITOR_CHANNEL_ID:
        content = message.content or ""
        if not content and message.embeds:
            for e in message.embeds:
                content += f" {e.title or ''} {e.description or ''}"
        
        if not content.strip(): return

        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(f"[{message.created_at}] {content.strip()}\n")

        save_channel = client.get_channel(SAVE_CHANNEL_ID)
        if save_channel:
            await save_channel.send(content="📂 **Log Updated**", file=discord.File(FILE_NAME))

# Start the web server and the bot
Thread(target=run_web).start()
client.run(TOKEN)
