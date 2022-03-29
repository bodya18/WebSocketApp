from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from middleware.config import mysql_conf
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Chat(db.Model):
    __tablename__ = 'Chats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))

    def __init__(self, title, status):
        self.title = title
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)



class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    socket = db.Column(db.Text(collation="utf8mb4_unicode_ci"))

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)



class Message(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    file = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    chat_id = db.Column(db.Integer(), db.ForeignKey("Chats.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)

    def __init__(self, message, status, file, chat_id, user_id):
        self.message = message
        self.status = status
        self.file = file
        self.user_id = user_id
        self.chat_id = chat_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Chat_User(db.Model):
    __tablename__ = 'Chat_User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey("Chats.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)

    def __init__(self, chat_id, user_id):
        self.user_id = user_id
        self.chat_id = chat_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

if __name__ == '__main__':
    app.run()