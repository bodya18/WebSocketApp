from database.models import User, db_session

class UserService:
    
    def addUser(name):
        user = User(name)
        db_session.add(user)
        db_session.commit()

    def getAll():
        return User.query.all()