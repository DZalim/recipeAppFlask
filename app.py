from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
CORS(app)
