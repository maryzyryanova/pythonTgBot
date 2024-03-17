import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from containers import Container
from handlers import (
    start_command,
    enter_name,
    enter_username,
    create_task,
    handle_task_title,
    handle_task_description
)
from services.user_states_service import UserStatesService

load_dotenv()

app: Client = Client(
    'my_account',
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
)

container = Container()
container.init_resources()
container.wire(modules=[__name__])

app.add_handler(
    MessageHandler(
        start_command,
        filters.command('start')
    )
)

app.add_handler(
    MessageHandler(
        create_task,
        filters.command('create_task')
    )
)

app.add_handler(
    MessageHandler(
        enter_name,
        filters.text & filters.create(
            lambda _, __, query: UserStatesService.get_user_state(query.from_user.id) == 'enter_name')
    )
)


app.add_handler(
    MessageHandler(
        enter_username,
        filters.text & filters.create(
            lambda _, __, query: UserStatesService.get_user_state(query.from_user.id) == 'enter_username')
    )
)

app.add_handler(
    MessageHandler(
        handle_task_title,
        filters.text & filters.create(
            lambda _, __, query: UserStatesService.get_user_state(query.from_user.id) == 'create_task_title'
        )
    )
)


app.add_handler(
    MessageHandler(
        handle_task_description,
        filters.text & filters.create(
            lambda _, __, query: UserStatesService.get_user_state(query.from_user.id) == 'create_task_description'
        )
    )
)

app.run()
