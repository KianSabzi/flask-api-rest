from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    userIdentifier = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship("TaskModel", back_populates="user", lazy="dynamic" , cascade="all, delete")
    categories = db.relationship("CategoryModel", back_populates="user", lazy="dynamic" , cascade="all, delete")
