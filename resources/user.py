import random , uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

from extension import SMS_Utility


from db import db
from models import UserModel
from schemas import UserSchema,UserUpdateSchema,UserRegisterSchema,UserVerifySchema


blp = Blueprint("Users", "users", description="Operations on users") 


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.phone_number == user_data["phone_number"]).first():
            abort(400, message="A user with that phone number already exists. please log in instead")
                    
        code_status = SMS_Utility.send_otp(self,user_data=user_data)
        if(int(code_status) > 2000):
            return {"message": "Code send successfully."}, 201
        else :
            return {"message": "There is a problem. please try again"}
               
@blp.route("/verify")
class VerifyUserPhone(MethodView):
    @blp.arguments(UserVerifySchema)
    def post(self, user_data):
        verify_result = SMS_Utility.verify_otp(self,user_data=user_data)        
        if(verify_result):
            user = UserModel.query.filter(UserModel.phone_number == user_data["phone_number"]).first()
            if user :
                additional_claims = {"uid": user.user_identifier}
                access_token = create_access_token(identity=user.id, fresh=True, additional_claims=additional_claims)
                refresh_token = create_refresh_token(user.id)
                return jsonify( access_token= access_token , refresh_token = refresh_token) , 200
            else:
                user = UserModel(user_identifier = str(uuid.uuid1()),
                                phone_number=user_data["phone_number"]            
                                 )
                try:
                    db.session.add(user)
                    db.session.commit()

                except SQLAlchemyError:
                     abort(500, message="An error occurred while register new user. please try again")
                
                return {"message": "User created successfully."}, 201
            
        else:
            abort(400, message="A code is in correct or expired. please try again")
        # print(user.user_identifier)
        # usercode= random.randint(int('1'+'0'*(7-1)), int('9'*7)),    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if(user_data.get("username") and user_data.get("password")):

            user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

            if user and pbkdf2_sha256.verify(user_data.get("password"), user.password):

                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200

            abort(401, message="Invalid credentials.")

        elif(user_data.get("phone_number")):

            user = UserModel.query.filter(UserModel.phone_number == user_data["phone_number"]).first()

            if user is None:
                abort(400, message="A user does not exist. please register first")
            else:
                code_status = SMS_Utility.send_otp(self,user_data=user_data)
                if(int(code_status) > 2000):
                    return {"message": "Code send successfully."}, 201
                else :
                    return {"message": "There is a problem. please try again"}



@blp.route("/user/<string:user_identifier>")
class UpdateUserInfo(MethodView):
    @blp.arguments(UserUpdateSchema)
    @blp.response(200,UserSchema)
    @jwt_required()
    def put(self, user_data, user_identifier):
        current_identity = get_jwt_identity()
        user = UserModel.query.filter(UserModel.user_identifier == user_identifier, UserModel.id == current_identity).first()
        # if user set the email for the first time the task was created and push to queue 
        # for send notification and update to user email.        
        if user.username is None:
            user.username = user_data.get("username")
            user.password = pbkdf2_sha256.hash(user_data.get("password"))
            user.email = user_data.get("email")
            db.session.commit()
            return user
        # if user change the email address the task queue was update base on new email.
        else:
            user.password = pbkdf2_sha256.hash(user_data.get("password"))
            user.email = user_data.get("email")
            db.session.commit()
            return user

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