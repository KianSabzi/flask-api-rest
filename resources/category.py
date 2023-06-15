import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategorySchema, CategoryUpdateSchema
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import CategoryModel


blp = Blueprint("Categories", __name__, description="Operations on categories")

@blp.route("/category/<string:category_id>")
class Category(MethodView):
    @blp.response(200,CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
       category = CategoryModel.query.get_or_404(category_id)
       db.session.delete(category)
       db.session.commit()

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200,CategorySchema)
    def put(self, category_data, category_id):
        
       category = CategoryModel.query.get_or_404(category_id)
       if category:
           category.name = category_data["name"]
       else:
           category = CategoryModel(id=category_id, **category_data)
           db.session.add(category)
           db.session.commit()

       return category

@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200,CategorySchema(many=True)) 
    def get(self):
        return CategoryModel.query.all()
    
    @blp.arguments(CategorySchema)
    @blp.response(201,CategorySchema)
    def post(self, category_data):
         
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category
    
    