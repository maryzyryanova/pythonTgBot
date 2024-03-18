from uuid import UUID

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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


def tasks_list(
        client: Client,
        message: Message
):
    current_user_id: int = message.from_user.id
    tasks: list[Tasks] = TaskService.get_all_tasks(current_user_id)
    task_buttons: list = []
    for task in tasks:
        task_buttons.append([InlineKeyboardButton(task.name, callback_data=f"view_task_{task.id}")])
    tasks_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(task_buttons)
    if tasks_markup:
        message.reply_text("Your tasks:", reply_markup=tasks_markup)
    else:
        message.reply_text("You don't have any tasks yet.")


def view_task(
    client: Client,
    callback_query: CallbackQuery
):
    task_id: str = callback_query.data.split("_")[2]

    try:
        task_id: UUID = UUID(task_id)
        task: Tasks = TaskService.get_task_by_id(task_id)
    except ValueError:
        callback_query.answer("Invalid task ID format!", show_alert=True)
        return

    if task:
        message_text = f"{task.name}\n{task.description}"
        commands_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Mark as Completed", callback_data=f"complete_task_{task_id}")],
                [InlineKeyboardButton("Delete Task", callback_data=f"delete_task_{task_id}")],
                [InlineKeyboardButton("Back to Task List", callback_data="tasks_list")]
            ]
        )
        callback_query.message.edit_text(message_text, reply_markup=commands_markup)
    else:
        callback_query.answer("Task not found!", show_alert=True)


def delete_task(
    client: Client,
    message: Message
):
    ...


def mark_task_as_completed(
    client: Client,
    message: Message
):
    ...
