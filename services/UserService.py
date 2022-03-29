from database.models import User, db_session

class UserService:
    
    def addUser(name, socket):
        user = User(name, socket)
        db_session.add(user)
        db_session.commit()
        return user.id

    def getAll():
        return User.query.all()

    
    def deleteUser(id):
        User.query.filter_by(id=id).delete()