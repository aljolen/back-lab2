from flask import request
from marshmallow import ValidationError

from webapp import app
from webapp.core.data import categories
from webapp.core.schemas import CategorySchema

category_schema = CategorySchema()


@app.get("/category/<id>")
def get_category(id):
    try:
        return category_schema.dump(categories[id])
    except KeyError:
        return {"message": f"Category with this id does not exist: <{id}>"}, 404


@app.delete("/category/<id>")
def delete_category(id):
    try:
        return category_schema.dump(categories.pop(id))
    except KeyError:
        return {"message": f"Category with this id does not exist: <{id}>"}, 404


@app.post("/category")
def create_category():
    category_data = request.get_json()
    if not category_data: return {"message": "No input data provided"}, 404
    try:
        category = category_schema.load(category_data)
    except ValidationError as err:
        return err.messages, 422

    categories[category.id] = category
    return category_schema.dump(category)


@app.get("/categories")
def get_categories():
    owner_id = request.args.get("owner_id")
    common = list(filter(lambda x: not x.owner_id or owner_id == x.owner_id, categories.values()))
    return category_schema.dump(common, many=True)
