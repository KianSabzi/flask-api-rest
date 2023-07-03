import random , uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from dotenv import load_dotenv
import os
import zeep


from db import db
from models import UserModel
from schemas import UserRegisterSchema,UserVerifySchema


blp = Blueprint("Users", "users", description="Operations on users") 


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        load_dotenv()
        if UserModel.query.filter(UserModel.phone_number == user_data["phone_number"]).first():
            abort(400, message="A user with that phone number already exists. please log in instead")
        print(os.getenv("S_WEBSERVICE_URL"))
        rclient = zeep.Client(os.getenv("S_WEBSERVICE_URL"))
        register_result = rclient.service.AutoSendCode(os.getenv("USERNAME"),os.getenv("PASSWORD"), 
                                                user_data["phone_number"],os.getenv("FOOTER_MSG"))
        if(int(register_result) > 2000):
            print(register_result)
            return {"message": "Code send successfully."}, 201
            
    
@blp.route("/verify")
class VerifyUserPhone(MethodView):
    @blp.arguments(UserVerifySchema)
    def post(self, user_data):
        load_dotenv()
        vclient = zeep.Client(os.getenv("S_WEBSERVICE_URL"))
        verify_result = vclient.service.CheckSendCode(os.getenv("USERNAME"),os.getenv("PASSWORD"), 
                                                user_data["phone_number"],user_data["code"])
        
        if(verify_result):
            user = UserModel(
            user_identifier = str(uuid.uuid1()),
            phone_number=user_data["phone_number"]            
        )
        # print(user.user_identifier)
        # usercode= random.randint(int('1'+'0'*(7-1)), int('9'*7)),
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while register new user. please try again")

        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        additional_claims = {"uid": user.user_identifier}
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

    @blp.response(200, UserRegisterSchema)
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