import uuid

from flask import request

from webapp import app
from webapp.utils import generate_users


users = dict(generate_users(["Alpha", "Beta", "Gamma", "Delta"]))

@app.post("/user")
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return user


@app.get("/users")
def get_users():
    return list(users.values())
