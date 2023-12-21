from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from webapp.core.model import RecordModel, CategoryModel, UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = False
        load_instance = True

    id = auto_field(dump_only=True)
    password = auto_field(load_only=True)

    @pre_load
    def preprocess(self, data, **kwargs):
        if 'password' in data:
            data['password'] = pbkdf2_sha256.hash(data["password"])
        return data

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        include_relationships = True
        include_fk = True
        load_instance = True

    id = auto_field(dump_only=True)


class RecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecordModel
        include_relationships = True
        include_fk = True
        load_instance = True

    id = auto_field(dump_only=True)
    created = auto_field(dump_only=True)
