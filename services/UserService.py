import datetime
from database.models import Message, User, File, session
from sqlalchemy import select
from middleware.config import log

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

    def new_message(message, user_id, file, status = None):
        msg = Message(message=message, user_id=user_id, status=status, date=datetime.datetime.now())
        session.add(msg)
        session.commit()
        if file:
            for one_file in file:
                added_file = File(name=one_file, message_id=msg.id)
                session.add(added_file)
                session.commit()

    def get_messages_by_userId(user_id):
        stmt = select(Message).where(Message.user_id == user_id)
        result = session.execute(stmt).scalars().all()
        return result

    def update_socket(socket, id):
        log.info(f"update_socket: {socket}, user: {id}")
        try:
            connection = session.connection()
            stmt = select(User).where(User.id == id)
            user = session.execute(stmt).scalars().one_or_none()
            log.info(f"user: {user}")
            if user:
                user.socket = socket
                session.add(user)
                session.commit()
        except Exception as e:
            log.error(f"update_socket_error: {e}")
        finally:
            connection.close()
        

    def update_status(status, id):
        stmt = select(User).where(User.id == id)
        user = session.execute(stmt).scalars().one_or_none()
        if user:
            user.status = status
            session.add(user)
            session.commit()
            return user.serialize()
        else:
            return None
        

    
    def delete_socket(socket):
        stmt = select(User).where(User.socket == socket)
        user = session.execute(stmt).scalars().one_or_none()
        if user:
            user.socket = None
            session.add(user)
            session.commit()
        else:
            return dict(error="User is not defined")

    def get_by_id(id):
        return User.get_by_id(id)

    def get_by_email(email):
        stmt = select(User).where(User.email == email)
        user = session.execute(stmt).scalars().one_or_none()
        return user