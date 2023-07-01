from datetime import datetime
import uuid
from flask import request , jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TaskSchema, TaskUpdateSchema,PlainTaskSchema,PlainCategorySchema
# from sqlalchemy import or_,and_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required , get_jwt_identity

from db import db
from models import TaskModel,CategoryModel


blp = Blueprint("Tasks", __name__, description="Operations on user tasks")

@blp.route("/task/<int:task_id>")
class Task(MethodView):
    @blp.response(200,TaskSchema)
    @jwt_required()
    def get(self, task_id):
        current_identity = get_jwt_identity()
        task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == current_identity).first()
        return task
    @jwt_required()
    def delete(self, task_id):
       current_identity = get_jwt_identity()
       task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == current_identity).first()
       db.session.delete(task)
       db.session.commit()
       return {"message": "Task deleted."}
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200,TaskSchema)
    @jwt_required()
    def put(self,task_data,task_id):
        current_identity = get_jwt_identity()
        task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == current_identity).first()
        if task:
            task.priority = task_data["priority"]
            task.name = task_data["name"]
            task.isDone = task_data["isDone"]
            task.dueDate = task_data["dueDate"]
            task.notif = task_data["notif"]
            task.notifPeriod = task_data["notifPeriod"]
            task.category_id = task_data["category_id"]
        else:
            task = TaskModel(id = task_id, user_id = current_identity, **task_data)
            db.session.add(task)
            db.session.commit()
        return task        

@blp.route("/task")
class TaskList(MethodView):
    @blp.response(200, PlainTaskSchema(many=True))
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        return TaskModel.query.filter(TaskModel.user_id == current_identity).all()

    
    @blp.arguments(TaskSchema)
    @blp.response(201,TaskSchema)
    @jwt_required()
    def post(self, task_data):
        current_identity = get_jwt_identity()
        # print(task_data["category_id"])
        if task_data["category_id"] :
            # user_category = CategoryModel.query.filter(
            #                     and_(
            #                     CategoryModel.id == task_data["category_id"] ,
            #                     CategoryModel.user_id == current_identity
            #                     )
            #                 ).first()
            user_category = CategoryModel.query.filter(                                
                                CategoryModel.id == task_data["category_id"] ,
                                CategoryModel.user_id == current_identity
                            ).first()
            if not user_category:
                abort(404, message="The category you selected does not exist.")
        # print(current_identity)
        task = TaskModel(user_id = current_identity, **task_data)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task.")

        return task