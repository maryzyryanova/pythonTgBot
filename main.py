import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from handlers import (
    start_command,
    enter_name,
    enter_username,
    create_task,
    handle_task_title,
    handle_task_description,
    tasks_list,
    view_task
)
from services.user_states_service import UserStatesService

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
        create_task,
        filters.command('create_task')
    )
)

app.add_handler(
    MessageHandler(
        tasks_list,
        filters.command('tasks_list')
    )
)


app.add_handler(
    CallbackQueryHandler(
        view_task,
        filters.regex(r'^view_task_\d+')
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
