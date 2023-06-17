from datetime import datetime
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TaskSchema, TaskUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel


blp = Blueprint("Tasks", __name__, description="Operations on tasks")

@blp.route("/task/<int:task_id>")
class Task(MethodView):
    @blp.response(200,TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task
    def delete(self, task_id):
       task = TaskModel.query.get_or_404(task_id)
       db.session.delete(task)
       db.session.commit()
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200,TaskSchema)
    def put(self,task_data, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            task.priority = task_data["priority"]
            task.name = task_data["name"]
            task.isDone = task_data["isDone"]
            task.dueDate = task_data["dueDate"]
            task.notif = task_data["notif"]
            task.notifPeriod = task_data["notifPeriod"]
            task.category_id = task_data["category_id"]
        else:
            task = TaskModel(id = task_id, **task_data)
            db.session.add(task)
            db.session.commit()
        return task        


@blp.route("/task")
class TaskList(MethodView):
    @blp.response(200,TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()

    
    @blp.arguments(TaskSchema)
    @blp.response(201,TaskSchema)
    def post(self,task_data):
        task = TaskModel(**task_data)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task.")

        return task
    
    