from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from webapp import app, db, jwt
from webapp.core.model import UserModel
from webapp.core.schemas import UserSchema

user_schema = UserSchema()


@app.get("/user/<int:id>")
@jwt_required()
def get_user(id):
    if id != get_jwt_identity(): return {"message": f"Not allowed"}, 401
    user = UserModel.query.get(id)
    if not user: return {"message": f"User with this id does not exist: <{id}>"}, 404
    return user_schema.dump(user)


@app.delete("/user/<int:id>")
@jwt_required()
def delete_user(id):
    if id != get_jwt_identity(): return {"message": f"Not allowed"}, 401
    user = UserModel.query.get(id)
    if not user: return {"message": f"User with this id does not exist: <{id}>"}, 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.dump(user)


@app.get("/users")
@jwt_required()
def get_users():
    return user_schema.dump(UserModel.query.all(), many=True)


@app.post("/users/register")
def register_user():
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
        return {"message": f"User with id {user.id} already exists"}, 500

    return user_schema.dump(user)


@app.post("/users/login/")
def login_user():
    credentials = request.get_json()
    id, password = credentials["id"], credentials["password"]
    user = UserModel.query.get(id)
    if not user: return {"message": f"User with this id does not exist: <{id}>"}, 404

    if not pbkdf2_sha256.verify(password, user.password):
        return {"message": "Invalid username or password"}, 401

    access_token = create_access_token(identity=user.id)

    return {
        "access_token": access_token,
        "message": "Authentication successful"
    }


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"message": "The token has expired.", "error": "token_expired"}, 401,



@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"message": "Signature verification failed.", "error": "invalid_token"}, 401



@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }, 401

