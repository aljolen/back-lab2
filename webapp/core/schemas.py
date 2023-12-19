from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from webapp.core.model import RecordModel, CategoryModel, UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = False
        load_instance = True

    id = auto_field(dump_only=True)

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
