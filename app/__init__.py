from flask import Flask
from app.routes import api_blueprints
from app import controllers
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_blueprints)

from app import routes
