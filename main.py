import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from handlers import start_command, enter_name, enter_username, get_user_state

load_dotenv()

app: Client = Client(
    'my_account',
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
)

app.add_handler(
    MessageHandler(
        start_command,
        filters.command('start')
    )
)

app.add_handler(
    MessageHandler(
        enter_name,
        filters.text & filters.create(lambda _, __, query: get_user_state(query.from_user.id) == 'enter_name')
    )
)


app.add_handler(
    MessageHandler(
        enter_username,
        filters.text & filters.create(lambda _, __, query: get_user_state(query.from_user.id) == 'enter_username')
    )
)
app.run()
