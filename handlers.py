import uuid

from pyrogram import Client
from pyrogram.types import Message

from fsm import RegisterFSM, TaskCreationFSM
from models import Tasks
from services.task_service import TaskService
from services.user_service import UserService
from services.user_states_service import UserStatesService


def start_command(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)

    if current_user_state != 'registered':
        if current_user_state is None:
            register_fsm = RegisterFSM()
            register_fsm.start_registration()
            current_user_state = register_fsm.state
            UserStatesService.create_user_state(current_user_id, current_user_state)
            message.reply_text("Let's start a registration process. Please, enter your name:")

        else:
            message.reply_text("Continue registration!")
    else:
        message.reply_text("You're registered!")


def enter_name(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)
    name = message.text
    UserService.create_new_user(current_user_id, name=name)
    register_fsm = RegisterFSM(initial=current_user_state)
    register_fsm.provide_name()
    current_user_state = register_fsm.state
    UserStatesService.update_user_state(current_user_id, current_user_state)
    message.reply_text("Great! Now, please enter your username:")


def enter_username(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)
    username: str = message.text
    if UserService.is_username_exists(username):
        message.reply_text("Username already exists! Try the new one!")
    else:
        UserService.update_username(current_user_id, username)
        register_fsm = RegisterFSM(initial=current_user_state)
        register_fsm.provide_username()
        current_user_state = register_fsm.state
        UserStatesService.update_user_state(current_user_id, current_user_state)
        message.reply_text("Congratulations! You're now registered!")


def create_task(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)

    if current_user_state == 'registered':
        message.reply_text("Enter task title:")
        task_creation_fsm: TaskCreationFSM = TaskCreationFSM()
        task_creation_fsm.create_new_task()
        current_user_state = task_creation_fsm.state
        UserStatesService.update_user_state(current_user_id, current_user_state)
    else:
        message.reply_text("You need to register first!")


def handle_task_title(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)

    task_title: str = message.text
    TaskService.create_task(current_user_id, task_title)
    task_creation_fsm: TaskCreationFSM = TaskCreationFSM(initial=current_user_state)
    task_creation_fsm.provide_task_title()
    current_user_state = task_creation_fsm.state
    UserStatesService.update_user_state(current_user_id, current_user_state)
    message.reply_text("Enter task description:")


def handle_task_description(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    current_user_state: str = UserStatesService.get_user_state(current_user_id)

    task_description: str = message.text
    the_last_task: Tasks = TaskService.get_the_last_task(current_user_id)
    the_last_task.description = task_description
    task_creation_fsm: TaskCreationFSM = TaskCreationFSM(initial=current_user_state)
    task_creation_fsm.provide_task_description()
    current_user_state = task_creation_fsm.state
    UserStatesService.update_user_state(current_user_id, current_user_state)
    message.reply_text("Task created successfully!")
