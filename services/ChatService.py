from database.models import Chat, db_session

class ChatService:
    
    def addChat(title):
        chat = Chat(title)
        db_session.add(chat)
        db_session.commit()

    def getAll():
        return Chat.query.all()

    def get_by_id(id):
        return Chat.query.filter_by(id=id).first()