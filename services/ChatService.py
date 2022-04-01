from database.models import Chat, session
from sqlalchemy import select

class ChatService:
    
    def addChat(title):
        chat = Chat(title)
        session.add(chat)
        session.commit()

    def getAll():
        chat = select(Chat)
        result = session.execute(chat).scalars().all()
        return result

    def get_by_id(id):
        stmt = select(Chat).where(Chat.id == id)
        result = session.execute(stmt).scalars().one_or_none()
        return result