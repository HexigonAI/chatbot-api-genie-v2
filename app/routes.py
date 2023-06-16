from flask import Blueprint
from app.controllers.ChatBotHandler import chat

api_blueprints = Blueprint('api_blueprints',__name__)

api_blueprints.add_url_rule('/chat', view_func=chat, methods=['POST'])

