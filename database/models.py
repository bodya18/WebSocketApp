from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, TEXT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from middleware.config import mysql_conf

engine = create_engine(mysql_conf, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


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

    def __init__(self, name, status = None):
        self.name = name
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)



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