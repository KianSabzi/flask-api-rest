import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategorySchema, CategoryUpdateSchema , TaskSchema
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import CategoryModel, UserModel


blp = Blueprint("Categories", __name__, description="Operations on user categories")

@blp.route("/category/<int:user_id>/<int:category_id>")
class Category(MethodView):
    @blp.response(200,CategorySchema)
    def get(self, user_id, category_id):
        category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == user_id).first()
        return category

    def delete(self, user_id, category_id):
       category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == user_id).first()
       db.session.delete(category)
       db.session.commit()
       return {"message": "Category deleted."}

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200,CategorySchema)
    def put(self, category_data, user_id, category_id):
        
       category = CategoryModel.query.filter(CategoryModel.id == category_id , CategoryModel.user_id == user_id).first()
       if category:
           category.name = category_data["name"]
       else:
           category = CategoryModel(id=category_id,user_id = user_id, **category_data)
           db.session.add(category)
           db.session.commit()

       return category

@blp.route("/category/<int:user_id>")
class CategoryList(MethodView):
    @blp.response(200,CategorySchema(many=True)) 
    def get(self, user_id):
        return CategoryModel.query.filter(CategoryModel.user_id == user_id).all()
    
    @blp.arguments(CategorySchema)
    @blp.response(201,CategorySchema)
    def post(self, category_data, user_id):
         
        category = CategoryModel(user_id = user_id,**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category    