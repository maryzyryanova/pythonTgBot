import datetime
import uuid

from connector import session
from models import Tasks


class TaskService:
    @staticmethod
    def create_task(current_user_id: int, task_title: str) -> None:
        task = Tasks(
            id=uuid.uuid4(),
            user_id=current_user_id,
            name=task_title,
            created_at=datetime.datetime.now()
        )
        session.add(task)
        session.commit()

    @staticmethod
    def get_the_last_task(current_user_id: int) -> Tasks:
        return session.query(Tasks).filter_by(user_id=current_user_id).order_by(Tasks.created_at.desc()).first()

    @staticmethod
    def get_all_tasks(current_user_id: int) -> list[Tasks]:
        return session.query(Tasks).filter_by(user_id=current_user_id).all()

    @staticmethod
    def get_task_by_id(task_id: uuid) -> Tasks:
        return session.query(Tasks).filter_by(id=task_id).first()

    @staticmethod
    def delete_task_by_id(task_id: uuid) -> bool:
        task: Tasks = TaskService.get_task_by_id(task_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def mark_task_as_completed(task_id: uuid) -> bool:
        task: Tasks = TaskService.get_task_by_id(task_id)
        if task:
            task.is_done = True
            session.add(task)
            session.commit()
            return True
        return False
