import discord

# --- CONFIG ---
# Remember to use a FRESH token from the Discord Developer Portal!
TOKEN = 'MTQ1NDc4MjEzNDcwNjM3MjcxMw.Gq_IN4.bE2jsbZhl3MuY0XiBX_uIGEoziFnOMh5pfLDGo' 
MONITOR_CHANNEL_ID = 1289705151027875972  
SAVE_CHANNEL_ID = 1454783709298561085     
FILE_NAME = "Trade_Logs.txt"

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Log Bot is live as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == MONITOR_CHANNEL_ID:
        content = message.content or ""
        if not content and message.embeds:
            for e in message.embeds:
                content += f" {e.title or ''} {e.description or ''}"
        
        if content.strip():
            with open(FILE_NAME, "a", encoding="utf-8") as f:
                f.write(f"[{message.created_at}] {content.strip()}\n")
            
            save_channel = client.get_channel(SAVE_CHANNEL_ID)
            if save_channel:
                await save_channel.send(file=discord.File(FILE_NAME))

client.run(TOKEN)
