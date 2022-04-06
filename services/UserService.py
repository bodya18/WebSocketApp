from database.models import Message, User, session
from sqlalchemy import select


class UserService:

    def addUser(name, email, role):
        user = User(name=name, email=email, role=role)
        session.add(user)
        session.commit()
        return user.serialize()

    def getAll():
        users = select(User)
        result = session.execute(users).scalars().all()
        return result

    def getStatus(status):
        users = select(User).where(User.status == status)
        result = session.execute(users).scalars().all()
        return result


    def get_admin(name, role):
        stmt = select(User).where(User.name == name, User.role == role)
        result = session.execute(stmt).scalars().one_or_none()
        return result

    
    def add_admin(name, password, role):
        user = User(name, password, role)
        session.add(user)
        session.commit()

    def new_message(message, user_id, status = None):
        msg = Message(message=message, user_id=user_id, status=status)
        session.add(msg)
        session.commit()

    def get_messages_by_userId(user_id):
        stmt = select(Message).where(Message.user_id == user_id)
        result = session.execute(stmt).scalars().all()
        return result

    def update_socket(socket, id):
        stmt = select(User).where(User.id == id)
        user = session.execute(stmt).scalars().one_or_none()
        if user:
            user.socket = socket
            session.add(user)
            session.commit()

    def update_status(status, id):
        stmt = select(User).where(User.id == id)
        user = session.execute(stmt).scalars().one_or_none()
        user.status = status
        session.add(user)
        session.commit()
        return user.serialize()

    
    def delete_socket(socket):
        stmt = select(User).where(User.socket == socket)
        user = session.execute(stmt).scalars().one_or_none()
        if user:
            user.socket = None
            session.add(user)
            session.commit()

    def get_by_id(id):
        return User.get_by_id(id)

    def get_by_email(email):
        stmt = select(User).where(User.email == email)
        user = session.execute(stmt).scalars().one_or_none()
        return user