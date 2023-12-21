from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from webapp import app, db
from webapp.core.model import RecordModel, CategoryModel
from webapp.core.schemas import RecordSchema

record_schema = RecordSchema()


@app.get("/record/<int:id>")
@jwt_required()
def get_record(id):
    user = RecordModel.query.get(id)
    if not user: return {"message": f"Record with this id does not exist: <{id}>"}, 404
    return record_schema.dump(user)


@app.delete("/record/<int:id>")
@jwt_required()
def delete_record(id):
    record = RecordModel.query.get(id)
    if not record: return {"message": f"Record with this id does not exist: <{id}>"}, 404
    db.session.delete(record)
    db.session.commit()
    return record_schema.dump(record)


@app.get("/records")
@jwt_required()
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    if not user_id and not category_id:
        return {
            "message": "At least one of the following query parameters should be present: [user_id, category_id]"}, 404
    if (user_id and not user_id.isnumeric()) or (category_id and not category_id.isnumeric()):
        return {
            "message": "Both parameters must be integers"}, 404

    records = RecordModel.query
    if category_id:
        records = records.filter(RecordModel.category_id == category_id)
    if user_id:
        records = records.filter(RecordModel.user_id == user_id)
    return record_schema.dump(records, many=True)


@app.post("/record")
@jwt_required()
def create_record():
    record_data = request.get_json()
    if not record_data: return {"message": "No input data provided"}, 404
    try:
        record = record_schema.load(record_data, session=db.session)
    except ValidationError as err:
        return err.messages, 422

    category = CategoryModel.query.get(record.category_id)
    if not category: return {"message": f"Category with id {record.category_id} does not exist"}, 404

    if category.owner_id and category.owner_id != record.user_id:
        return {
            "message": f"Category is not public and does not belong to the specified user. Category: {category.id}, User ({record.user_id}) != Owner({category.owner_id})"}

    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError:
        return {"message": f"User with given id {record.user_id} does not exist"}, 404

    return record_schema.dump(record)
