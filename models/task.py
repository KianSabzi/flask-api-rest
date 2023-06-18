from db import db
from datetime import datetime


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    priority = db.Column(db.Integer, unique=False, nullable=False)
    isDone = db.Column(db.Boolean,nullable=True)
    createDate = db.Column(db.DateTime, nullable=False,default=datetime.now())
    dueDate = db.Column(db.DateTime)
    notif = db.Column(db.Boolean)
    notifPeriod = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), unique=False, nullable=False)
    category = db.relationship("CategoryModel", back_populates="tasks")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="tasks")