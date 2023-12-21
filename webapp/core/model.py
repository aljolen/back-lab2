from sqlalchemy import func

from webapp import db


class UserModel(db.Model):
    __tablename__ = "users_v2"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class CategoryModel(db.Model):
    __tablename__ = "categories_v2"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users_v2.id"), unique=False, nullable=True)

class RecordModel(db.Model):
    __tablename__ = "records_v2"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users_v2.id"), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories_v2.id"), unique=False, nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=func.now())
    sum = db.Column(db.Integer, unique=False, nullable=False)
