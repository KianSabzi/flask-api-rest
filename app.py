from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta
import os,json
from dotenv import load_dotenv

from db import db
import models

from resources.task import blp as ItemBlueprint
from resources.category import blp as StoreBlueprint
from resources.user import blp as UserBlueprint

Access_Expires = timedelta(hours=1)

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config.from_file("settings.json", load=json.load)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Access_Expires

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    jwt = JWTManager(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


