from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from webapp import app, db
from webapp.core.model import CategoryModel
from webapp.core.schemas import CategorySchema

category_schema = CategorySchema()


@app.get("/category/<int:id>")
def get_category(id):
    category = CategoryModel.query.get(id)
    if not category: return {"message": f"Category with this id does not exist: <{id}>"}, 404
    return category_schema.dump(category)


@app.delete("/category/<int:id>")
def delete_category(id):
    category = CategoryModel.query.get(id)
    if not category: return {"message": f"Category with this id does not exist: <{id}>"}, 404
    db.session.delete(category)
    db.session.commit()
    return category_schema.dump(category)


@app.post("/category")
def create_category():
    category_data = request.get_json()
    if not category_data: return {"message": "No input data provided"}, 404
    try:
        category = category_schema.load(category_data, session=db.session)
    except ValidationError as err:
        return err.messages, 422

    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        return {"message": f"User with id {category.owner_id} does not exist"}, 404

    return category_schema.dump(category)


@app.get("/categories")
def get_categories():
    owner_id = request.args.get("owner_id")
    if owner_id and not owner_id.isnumeric(): return {"message": "Invalid id"}, 404
    common_and_user_defined = (CategoryModel
                               .query
                               .filter((CategoryModel.owner_id == owner_id)
                                       | (CategoryModel.owner_id == None))
                               )
    return category_schema.dump(common_and_user_defined, many=True)
