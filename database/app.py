from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from middleware.config import mysql_conf
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Chat(db.Model):
    __tablename__ = 'Chats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    password = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    email = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    role = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))


class Message(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    file = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    chat_id = db.Column(db.Integer(), db.ForeignKey("Chats.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)


class Chat_User(db.Model):
    __tablename__ = 'Chat_User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey("Chats.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)


if __name__ == '__main__':
    app.run()