import datetime
from database.models import Message, User, File, session
from sqlalchemy import select
from middleware.config import log

class UserService:

    def addUser(name, email, role):
        connection = session.connection()
        try:
            user = User(name=name, email=email, role=role)
            session.add(user)
            session.commit()
            return user.serialize()
        finally:
            connection.close()

    def getAll():
        connection = session.connection()
        try:
            users = select(User)
            result = session.execute(users).scalars().all()
            return result
        finally:
            connection.close()


    def getStatus(status):
        connection = session.connection()
        try:
            users = select(User).where(User.status == status)
            result = session.execute(users).scalars().all()
            return result
        finally:
            connection.close()


    def get_admin(name, role):
        connection = session.connection()
        try:
            stmt = select(User).where(User.name == name, User.role == role)
            result = session.execute(stmt).scalars().one_or_none()
            return result
        finally:
            connection.close()

    
    def add_admin(name, password, role):
        connection = session.connection()
        try:
            user = User(name, password, role)
            session.add(user)
            session.commit()
        finally:
            connection.close()


    def new_message(message, user_id, file, status = None):
        connection = session.connection()
        try:
            msg = Message(message=message, user_id=user_id, status=status, date=datetime.datetime.now())
            session.add(msg)
            session.commit()
            if file:
                for one_file in file:
                    added_file = File(name=one_file, message_id=msg.id)
                    session.add(added_file)
                    session.commit()
        finally:
            connection.close()


    def get_messages_by_userId(user_id):
        connection = session.connection()
        try:
            stmt = select(Message).where(Message.user_id == user_id)
            result = session.execute(stmt).scalars().all()
            return result
        finally:
            connection.close()


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
        connection = session.connection()
        try:
            stmt = select(User).where(User.id == id)
            user = session.execute(stmt).scalars().one_or_none()
            if user:
                user.status = status
                session.add(user)
                session.commit()
                return user.serialize()
            else:
                return None
        finally:
            connection.close()
       

    
    def delete_socket(socket):
        connection = session.connection()
        try:
            stmt = select(User).where(User.socket == socket)
            user = session.execute(stmt).scalars().one_or_none()
            if user:
                user.socket = None
                session.add(user)
                session.commit()
            else:
                return dict(error="User is not defined")
        finally:
            connection.close()

    def get_by_id(id):
        return User.get_by_id(id)

    def get_by_email(email):
        connection = session.connection()
        try:
            stmt = select(User).where(User.email == email)
            user = session.execute(stmt).scalars().one_or_none()
            return user
        finally:
            connection.close()