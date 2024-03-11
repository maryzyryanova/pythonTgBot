import os

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

app = Client(
    'my_account',
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
)


app.run()
