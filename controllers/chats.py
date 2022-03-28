from services.ChatService import ChatService
from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint, redirect, render_template, request, session
import json


chats_page = Blueprint('chats', __name__, template_folder='templates')

@chats_page.route('/', methods=['GET'])
def index_page():
    chats = ChatService.getAll()
    return render_template("index.html", chats=chats, session=session)


@chats_page.route('/chat/<id>', methods=['GET'])
def chat_page(id):
    users = UserService.getAll()
    chat = ChatService.get_by_id(id)
    return render_template("single_chat.html", chat = chat, users=users)


@chats_page.route('/new/chat/', methods=['POST'])
def add():
    chat_title = request.form.get('title')
    ChatService.addChat(chat_title)
    return redirect('/')