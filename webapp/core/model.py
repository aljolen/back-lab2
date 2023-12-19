from sqlalchemy import func

from webapp import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)


class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=True)

class RecordModel(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), unique=False, nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=func.now())
    sum = db.Column(db.Integer, unique=False, nullable=False)
