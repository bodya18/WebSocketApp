from click import echo
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, TEXT
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from middleware.config import mysql_conf

engine = create_engine(mysql_conf, convert_unicode=True, echo=False)
session = Session(engine)
Base = declarative_base()


class Chat(Base):
    __tablename__ = 'Chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255, collation="utf8mb4_unicode_ci"))
    status = Column(String(255, collation="utf8mb4_unicode_ci"))

    def __init__(self, title, status = None):
        self.title = title
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)
        



class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255, collation="utf8mb4_unicode_ci"))
    status = Column(String(255, collation="utf8mb4_unicode_ci"))
    password = Column(String(255, collation="utf8mb4_unicode_ci"))
    email = Column(String(255, collation="utf8mb4_unicode_ci"))
    role = Column(String(255, collation="utf8mb4_unicode_ci"))

    def __init__(self, name, password = None, role = None, status = None):
        self.name = name
        self.password = password
        self.role = role
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
    def serialize(self):
        return dict(
            id = self.id,
            name = self.name,
            status = self.status,
            email = self.email,
            role = self.role,
        )



class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(255, collation="utf8mb4_unicode_ci"))
    status = Column(String(255, collation="utf8mb4_unicode_ci"))
    file = Column(String(255, collation="utf8mb4_unicode_ci"))
    chat_id = Column(Integer(), ForeignKey("Chats.id"), nullable=False)
    user_id = Column(Integer(), ForeignKey("Users.id"), nullable=False)

    def __init__(self, message, status = None, file = None, chat_id = None, user_id = None):
        self.message = message
        self.status = status
        self.file = file
        self.user_id = user_id
        self.chat_id = chat_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Chat_User(Base):
    __tablename__ = 'Chat_User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer(), ForeignKey("Chats.id"), nullable=False)
    user_id = Column(Integer(), ForeignKey("Users.id"), nullable=False)

    def __init__(self, chat_id, user_id):
        self.user_id = user_id
        self.chat_id = chat_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

Base.metadata.create_all(bind=engine)