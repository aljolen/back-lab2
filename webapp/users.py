from flask import request
from marshmallow import ValidationError

from webapp import app
from webapp.core.data import users
from webapp.core.schemas import UserSchema

user_schema = UserSchema()


@app.get("/user/<id>")
def get_user(id):
    try:
        return user_schema.dump(users[id])
    except KeyError:
        return {"message": f"User with this id does not exist: <{id}>"}, 404


@app.delete("/user/<id>")
def delete_user(id):
    try:
        return user_schema.dump(users.pop(id))
    except KeyError:
        return {"message": f"User with this id does not exist: <{id}>"}, 404


@app.post("/user")
def create_user():
    user_data = request.get_json()
    if not user_data: return {"message": "No input data provided"}, 404
    try:
        user = user_schema.load(user_data)
    except ValidationError as err:
        return err.messages, 422

    users[user.id] = user
    return user_schema.dump(user)


@app.get("/users")
def get_users():
    return user_schema.dump(users.values(), many=True)
