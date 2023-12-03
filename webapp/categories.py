import dataclasses

from flask import request

from webapp import app
from webapp.data import categories
from webapp.model import Category


@app.get("/category/<id>")
def get_category(id):
    return dataclasses.asdict(categories[id])


@app.delete("/category/<id>")
def delete_category(id):
    return dataclasses.asdict(categories.pop(id))


@app.post("/category")
def create_category():
    category_data = request.get_json()
    category = Category(**category_data)
    categories[category.id] = category
    return dataclasses.asdict(category)


@app.get("/categories")
def get_categories():
    return list(categories.values())
