import dataclasses

from flask import request

from webapp import app
from webapp.core.data import users
from webapp.core.model import User


@app.get("/user/<id>")
def get_user(id):
    return dataclasses.asdict(users[id])


@app.delete("/user/<id>")
def delete_user(id):
    return dataclasses.asdict(users.pop(id))


@app.post("/user")
def create_user():
    user_data = request.get_json()
    user = User(**user_data)
    users[user.id] = user
    return dataclasses.asdict(user)


@app.get("/users")
def get_users():
    return list(users.values())
