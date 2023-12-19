from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from webapp import app, db
from webapp.core.model import UserModel
from webapp.core.schemas import UserSchema

user_schema = UserSchema()


@app.get("/user/<int:id>")
def get_user(id):
    user = UserModel.query.get(id)
    if not user: return {"message": f"User with this id does not exist: <{id}>"}, 404
    return user_schema.dump(user)


@app.delete("/user/<int:id>")
def delete_user(id):
    user = UserModel.query.get(id)
    if not user: return {"message": f"User with this id does not exist: <{id}>"}, 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.dump(user)


@app.post("/user")
def create_user():
    user_data = request.get_json()
    if not user_data: return {"message": "No input data provided"}, 404
    try:
        user = user_schema.load(user_data, session=db.session)
    except ValidationError as err:
        return err.messages, 422

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return {"message": f"User with id {user.id} already exists"}, 404

    return user_schema.dump(user)


@app.get("/users")
def get_users():
    return user_schema.dump(UserModel.query.all(), many=True)
