import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategorySchema, CategoryUpdateSchema , TaskSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity


from db import db
from models import CategoryModel, UserModel


blp = Blueprint("Categories", __name__, description="Operations on user categories")

@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @blp.response(200,CategorySchema)
    @jwt_required()
    def get(self, category_id):
        current_identity = get_jwt_identity()
        # print(current_identity)
        category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == current_identity).first()
        return category
    @jwt_required()
    def delete(self, user_id, category_id):
       current_identity = get_jwt_identity()
       category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == current_identity).first()
       db.session.delete(category)
       db.session.commit()
       return {"message": "Category deleted."}

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200,CategorySchema)
    @jwt_required()
    def put(self, category_data, category_id):
       current_identity = get_jwt_identity()
       category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == current_identity).first()
       if category:
           category.name = category_data["name"]
       else:
           category = CategoryModel(id=category_id,user_id = current_identity, **category_data)
           db.session.add(category)
           db.session.commit()

       return category

@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200,CategorySchema(many=True)) 
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        print(current_identity)
        return CategoryModel.query.filter(CategoryModel.user_id == current_identity).all()
    
    @blp.arguments(CategorySchema)
    @blp.response(201,CategorySchema)
    @jwt_required()
    def post(self, category_data):

        current_identity = get_jwt_identity() 
        category = CategoryModel(user_id = current_identity,**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category    