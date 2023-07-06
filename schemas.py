from marshmallow import Schema, fields ,validates, ValidationError
from marshmallow.validate import Length, Range,Regexp
from datetime import datetime


class PlainTaskSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=3,max=350))
    priority = fields.Int(required=True)
    isDone = fields.Bool()
    createDate = fields.DateTime(required = True)
    dueDate = fields.DateTime()
    notif = fields.Bool()
    notifPeriod = fields.Int()

    @validates('dueDate')
    def is_greater_than_current_date(value):
        """'value' is the datetime parsed from dueDate by marshmallow"""
        now = datetime.now()
        if value < now:
            raise ValidationError("due date must be greater than current time!")
        # if the function doesn't raise an error, the check is considered passed

class PlainCategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=3,max=80))
    user_id = fields.Str(dump_only=True)

class TaskSchema(PlainTaskSchema):
    category_id = fields.Int(required=True , load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)

class TaskUpdateSchema(Schema):
    name = fields.Str(validate=Length(min=3,max=350))
    isDone = fields.Bool()
    dueDate = fields.DateTime()
    notif = fields.Bool()
    notifPeriod = fields.Int()

    @validates('dueDate')
    def is_greater_than_current_date(value):
        """'value' is the datetime parsed from dueDate by marshmallow"""
        now = datetime.now()
        if value < now:
            raise ValidationError("due date must be greater than current time!")
        # if the function doesn't raise an error, the check is considered passed

class CategorySchema(PlainCategorySchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)    

class CategoryUpdateSchema(Schema):
    name = fields.Str(validate=Length(min=3, max=80))

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(validate=Length(min=4,max=80))
    user_identifier = fields.Str()
    password = fields.Str(load_only=True, validate=Length(min=4,max=80))
    email = fields.Email()
class UserUpdateSchema(Schema):
    username = fields.Str(validate=Length(min=4,max=80))
    password = fields.Str(load_only=True, validate=Length(min=4,max=80))
    email = fields.Email()

class UserRegisterSchema(UserSchema):
    phone_number = fields.Str( validate=Regexp('^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$'))

class UserVerifySchema(UserRegisterSchema):
    code = fields.Str(required=True)
