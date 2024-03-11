import uuid

from sqlalchemy import Column, UUID, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False, unique=False)
    username = Column(String(50), nullable=False, unique=True)


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False, unique=False)
    description = Column(Text, nullable=True, unique=False)
    state = Column(String(10), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
