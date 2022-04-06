from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, select, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from middleware.config import mysql_conf
import datetime

engine = create_engine(mysql_conf, convert_unicode=True, echo=False)
session = Session(engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255, collation="utf8mb4_unicode_ci"))
    status = Column(String(255, collation="utf8mb4_unicode_ci"))
    password = Column(String(255, collation="utf8mb4_unicode_ci"))
    email = Column(String(255, collation="utf8mb4_unicode_ci"))
    role = Column(String(255, collation="utf8mb4_unicode_ci"))
    socket = Column(String(255, collation="utf8mb4_unicode_ci"))

    def __init__(self, name, password = None, role = None, status = None, email=None):
        self.name = name
        self.password = password
        self.role = role
        self.status = status
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
    def serialize(self):
        return dict(
            id = self.id,
            name = self.name,
            status = self.status,
            email = self.email,
            role = self.role,
            socket = self.socket,
            last_message = Message.get_last_message(self.id),
        )
    
    def get_by_id(id):
        stmt = select(User).where(User.id == id)
        result = session.execute(stmt).scalars().one_or_none()
        return result.serialize()
    
    def drop_all_sockets():
        sclrs = select(User)
        users = session.execute(sclrs).scalars().all()
        for user in users:
            user.socket = None
            session.add(user)
            session.commit()



class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(255, collation="utf8mb4_unicode_ci"))
    status = Column(String(255, collation="utf8mb4_unicode_ci"))
    file = Column(String(255, collation="utf8mb4_unicode_ci"))
    user_id = Column(Integer(), ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(), default=datetime.datetime.now())

    def __init__(self, message, status = None, file = None, user_id = None):
        self.message = message
        self.status = status
        self.file = file
        self.user_id = user_id

    def serialize(self):
        return dict(
            id = self.id,
            message = self.message,
            status = self.status,
            file = self.file,
            user_id = self.user_id,
            date = str(self.date)
        )

    def get_last_message(user_id):
        stmt = select(Message).where(Message.user_id == user_id).order_by(Message.id.desc()).limit(1)
        result = session.execute(stmt).scalars().one_or_none()
        if result is None:
            return result
        return result.serialize()


Base.metadata.create_all(bind=engine)

User.drop_all_sockets()