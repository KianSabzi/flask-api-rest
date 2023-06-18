from datetime import datetime
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TaskSchema, TaskUpdateSchema,PlainTaskSchema
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel


blp = Blueprint("Tasks", __name__, description="Operations on user tasks")

@blp.route("/task/<int:user_id>/<int:task_id>")
class Task(MethodView):
    @blp.response(200,TaskSchema)
    def get(self, user_id, task_id):
        task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
        return task
    def delete(self, user_id, task_id):
       task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
       db.session.delete(task)
       db.session.commit()
       return {"message": "Task deleted."}
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200,TaskSchema)
    def put(self,task_data, user_id, task_id):
        task = TaskModel.query.filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
        if task:
            task.priority = task_data["priority"]
            task.name = task_data["name"]
            task.isDone = task_data["isDone"]
            task.dueDate = task_data["dueDate"]
            task.notif = task_data["notif"]
            task.notifPeriod = task_data["notifPeriod"]
            task.category_id = task_data["category_id"]
        else:
            task = TaskModel(id = task_id, user_id = user_id, **task_data)
            db.session.add(task)
            db.session.commit()
        return task        

@blp.route("/task/<int:user_id>")
class TaskList(MethodView):
    @blp.response(200, PlainTaskSchema(many=True))
    def get(self , user_id):
        return TaskModel.query.filter(TaskModel.user_id == user_id).all()

    
    @blp.arguments(TaskSchema)
    @blp.response(201,TaskSchema)
    def post(self, task_data , user_id):
        task = TaskModel(user_id = user_id, **task_data)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task.")

        return task