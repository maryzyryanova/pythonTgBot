from connector import session
from models import Users


class UserService:
    @staticmethod
    def create_new_user(current_user_id: int, name=None, username=None) -> None:
        user: Users = Users(
            id=current_user_id,
            name=name,
            username=username
        )
        session.add(user)
        session.commit()

    @staticmethod
    def get_user_by_id(current_user_id: int) -> Users:
        return session.query(Users).filter_by(id=current_user_id).first()

    @staticmethod
    def update_username(current_user_id: int, username: str) -> None:
        user_object: Users = UserService.get_user_by_id(current_user_id)
        user_object.username = username
        session.add(user_object)
        session.commit()

    @staticmethod
    def is_username_exists(username: str) -> bool:
        usernames = [result[0] for result in session.query(Users.username).all()]
        return username in usernames
