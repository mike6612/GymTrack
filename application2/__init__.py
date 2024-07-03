from flask import Flask
from project3config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

api = Api()

app2 = Flask(__name__)
app2.config.from_object(Config)


db = MongoEngine()
db.init_app(app2)
api.init_app(app2)

from application2 import routes2
