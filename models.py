import uuid

from sqlalchemy import Column, UUID, String, Text, ForeignKey, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=True, unique=False)
    username = Column(String(50), nullable=True, unique=True)


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False, unique=False)
    description = Column(Text, nullable=True, unique=False)
    state = Column(String(10), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))


class UsersStates(Base):
    __tablename__ = 'usersstates'

    user_id = Column(Integer, primary_key=True, unique=True)
    state = Column(String(50), nullable=False, unique=False)
