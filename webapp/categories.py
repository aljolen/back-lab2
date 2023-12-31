from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from webapp import app, db
from webapp.core.model import CategoryModel
from webapp.core.schemas import CategorySchema

category_schema = CategorySchema()


@app.get("/category/<int:id>")
@jwt_required()
def get_category(id):
    category = CategoryModel.query.get(id)
    if not category: return {"message": f"Category with this id does not exist: <{id}>"}, 404
    if category.owner_id and category.owner_id != get_jwt_identity(): return {"message": f"Not allowed"}, 401
    return category_schema.dump(category)


@app.delete("/category/<int:id>")
@jwt_required()
def delete_category(id):
    category = CategoryModel.query.get(id)
    if not category: return {"message": f"Category with this id does not exist: <{id}>"}, 404
    if category.owner_id != get_jwt_identity(): return {"message": f"Not allowed"}, 401
    db.session.delete(category)
    db.session.commit()
    return category_schema.dump(category)


@app.post("/category")
@jwt_required()
def create_category():
    category_data = request.get_json()
    if not category_data: return {"message": "No input data provided"}, 404
    try:
        category = category_schema.load(category_data, session=db.session)
    except ValidationError as err:
        return err.messages, 422

    if category.owner_id and category.owner_id != get_jwt_identity(): return {"message": f"Not allowed"}, 401
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        return {"message": f"User with id {category.owner_id} does not exist"}, 404

    return category_schema.dump(category)


@app.get("/categories")
@jwt_required()
def get_categories():
    owner_id = request.args.get("owner_id")
    if owner_id and not owner_id.isnumeric(): return {"message": "Invalid id"}, 404
    if owner_id and owner_id != get_jwt_identity(): return {"message": f"Not allowed"}, 401

    common_and_user_defined = (CategoryModel
                               .query
                               .filter((CategoryModel.owner_id == owner_id)
                                       | (CategoryModel.owner_id == None))
                               )
    return category_schema.dump(common_and_user_defined, many=True)
