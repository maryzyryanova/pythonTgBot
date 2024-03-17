from connector import session
from models import UsersStates


class UserStatesService:
    @staticmethod
    def get_users_states_object(current_user_id: int) -> UsersStates:
        return session.query(UsersStates).filter_by(user_id=current_user_id).first()

    @staticmethod
    def get_user_state(current_user_id: int) -> str:
        user_state_object: UsersStates = UserStatesService.get_users_states_object(current_user_id)
        return user_state_object.state if user_state_object else None

    @staticmethod
    def update_user_state(current_user_id: int, current_user_state: str) -> None:
        user_state_object: UsersStates = UserStatesService.get_users_states_object(current_user_id)
        user_state_object.state = current_user_state
        session.add(user_state_object)
        session.commit()

    @staticmethod
    def create_user_state(current_user_id: int, current_user_state: str) -> None:
        user_state_object: UsersStates = UsersStates(
            user_id=current_user_id,
            state=current_user_state
        )
        session.add(user_state_object)
        session.commit()
