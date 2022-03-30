from services.ChatService import ChatService
from services.UserService import UserService
from middleware.config import ROOT_DIR
from flask import Blueprint, redirect, render_template, request, session
import json


chats_page = Blueprint('chats', __name__, template_folder='templates')

@chats_page.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")