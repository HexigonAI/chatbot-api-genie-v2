from flask import Blueprint
from app.controllers.ChatBotHandler import chat, createEmbedding

api_blueprints = Blueprint('api_blueprints',__name__)

api_blueprints.add_url_rule('/create-embedding', view_func=createEmbedding, methods=['POST'])
api_blueprints.add_url_rule('/chat', view_func=chat, methods=['POST'])

