from marshmallow import Schema, fields


class PlainTaskSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    priority = fields.Int(required=True)
    isDone = fields.Bool()
    createDate = fields.DateTime(required = True)
    dueDate = fields.DateTime()
    notif = fields.Bool()
    notifPeriod = fields.Int()

class PlainCategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Str(dump_only=True)

class TaskSchema(PlainTaskSchema):
    category_id = fields.Int(required=True , load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)

class TaskUpdateSchema(Schema):
    name = fields.Str()
    isDone = fields.Bool()
    dueDate = fields.DateTime()
    notif = fields.Bool()
    notifPeriod = fields.Int()

class CategorySchema(PlainCategorySchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)    

class CategoryUpdateSchema(Schema):
    name = fields.Str()

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    user_identifier = fields.Str()
    password = fields.Str(required=True,load_only=True)
