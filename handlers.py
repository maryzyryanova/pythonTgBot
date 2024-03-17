from dependency_injector.wiring import Provide, inject
from pyrogram import Client
from pyrogram.types import Message
from fsm import RegisterFSM
from services.user_service import UserService
from services.user_states_service import UserStatesService
from containers import Container


@inject
def start_command(
        client: Client,
        message: Message,
        user_state_service: UserStatesService = Provide[Container.user_states_service]
):
    current_user_id: int = message.from_user.id
    current_user_state: str = user_state_service.get_user_state(current_user_id)

    if current_user_state != 'registered':
        if current_user_state is None:
            register_fsm = RegisterFSM()
            register_fsm.start_registration()
            current_user_state = register_fsm.state
            user_state_service.create_user_state(current_user_id, current_user_state)
            message.reply_text("Let's start a registration process. Please, enter your name:")

        else:
            message.reply_text("Continue registration!")
    else:
        message.reply_text("You're registered!")


@inject
def enter_name(
        client: Client,
        message: Message,
        user_state_service: UserStatesService = Provide[Container.user_states_service],
        user_service: UserService = Provide[Container.user_service]
):
    current_user_id: int = message.from_user.id
    current_user_state: str = user_state_service.get_user_state(current_user_id)
    name = message.text
    user_service.create_new_user(current_user_id, name=name)
    register_fsm = RegisterFSM(initial=current_user_state)
    register_fsm.provide_name()
    current_user_state = register_fsm.state
    user_state_service.update_user_state(current_user_id, current_user_state)
    message.reply_text("Great! Now, please enter your username:")


@inject
def enter_username(
        client: Client,
        message: Message,
        user_state_service: UserStatesService = Provide[Container.user_states_service],
        user_service: UserService = Provide[Container.user_service]
):
    current_user_id: int = message.from_user.id
    current_user_state: str = user_state_service.get_user_state(current_user_id)
    username: str = message.text
    if user_service.is_username_exists(username):
        message.reply_text("Username already exists! Try the new one!")
    else:
        user_service.update_username(current_user_id, username)
        register_fsm = RegisterFSM(initial=current_user_state)
        register_fsm.provide_username()
        current_user_state = register_fsm.state
        user_state_service.update_user_state(current_user_id, current_user_state)
        message.reply_text("Congratulations! You're now registered!")
