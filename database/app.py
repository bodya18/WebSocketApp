import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from middleware.config import mysql_conf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_conf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    password = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    email = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    role = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    socket = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    site_id = db.Column(db.Integer(), db.ForeignKey("Sites.id"))

class Message(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text(collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now())

class File(db.Model):
    __tablename__ = 'Files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    message_id = db.Column(db.Integer(), db.ForeignKey("Messages.id"), nullable=False)

class Site(db.Model):
    __tablename__ = 'Sites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    status = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    url = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))

class Setting(db.Model):
    __tablename__ = 'Settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))
    base_value = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))


class Site_Setting(db.Model):
    __tablename__ = 'SiteSettings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.Integer(), db.ForeignKey("Sites.id", ondelete="CASCADE"))
    setting_id = db.Column(db.Integer(), db.ForeignKey("Settings.id", ondelete="CASCADE"))
    value = db.Column(db.String(255, collation="utf8mb4_unicode_ci"))


if __name__ == '__main__':
    app.run()