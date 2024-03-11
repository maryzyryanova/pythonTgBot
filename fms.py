from transitions import Machine


class Matter(object):
    pass


lump = Matter()

register_states = ['waiting_name', 'waiting_username', 'successful_login']
register_transitions = [
    {'trigger': 'name_is_entered', 'source': 'waiting_name', 'destination': 'waiting_username'},
    {'trigger': 'username_is_entered', 'source': 'waiting_username', 'destination': 'successful_login'}
]

register_machine = Machine(lump, states=register_states, transitions=register_transitions, initial='waiting_name')
