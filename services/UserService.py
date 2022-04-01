from database.models import User, session
from sqlalchemy import select


class UserService:

    def addUser(name, email, role):
        user = User(name=name, email=email, role=role)
        session.add(user)
        session.commit()
        return user.id

    def getAll():
        users = select(User)
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