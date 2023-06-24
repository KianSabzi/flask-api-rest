import random , uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users") 


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(400, message="A user with that username already exists.")

        user = UserModel(
            userIdentifier = str(uuid.uuid1()),
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        print(user.userIdentifier)
        # usercode= random.randint(int('1'+'0'*(7-1)), int('9'*7)),
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task.")

        return {"message": "User created successfully."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        additional_claims = {"uid": user.userIdentifier}
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims=additional_claims)
            refresh_token = create_refresh_token(user.id)
            return jsonify( access_token= access_token , refresh_token = refresh_token) , 200
        
        abort(401, message="Invalid credentials.")
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200