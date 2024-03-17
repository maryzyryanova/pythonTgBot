from transitions import Machine


class RegisterFSM(object):
    __states: list[str] = ['start', 'enter_name', 'enter_username', 'registered']
    __transitions: list[dict[str, str]] = [
        {'trigger': 'start_registration', 'source': 'start', 'dest': 'enter_name'},
        {'trigger': 'provide_name', 'source': 'enter_name', 'dest': 'enter_username'},
        {'trigger': 'provide_username', 'source': 'enter_username', 'dest': 'registered'},
    ]

    def __init__(self, initial: str = 'start'):
        self.register_machine = Machine(
            model=self,
            states=self.__states,
            transitions=self.__transitions,
            initial=initial
        )


class TaskCreationFSM(object):
    __states: list[str] = ['new_task', 'create_task_title', 'create_task_description', 'registered']
    __transitions: list[dict[str, str]] = [
        {'trigger': 'create_new_task', 'source': 'new_task', 'dest': 'create_task_title'},
        {'trigger': 'provide_task_title', 'source': 'create_task_title', 'dest': 'create_task_description'},
        {'trigger': 'provide_task_description', 'source': 'create_task_description', 'dest': 'registered'},
    ]

    def __init__(self, initial: str = 'new_task'):
        self.register_machine = Machine(
            model=self,
            states=self.__states,
            transitions=self.__transitions,
            initial=initial
        )
