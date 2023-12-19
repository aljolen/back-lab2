from flask import request
from marshmallow import ValidationError

from webapp import app
from webapp.core.data import records, categories, users
from webapp.core.schemas import RecordSchema

record_schema = RecordSchema()


@app.get("/record/<id>")
def get_record(id):
    try:
        return record_schema.dump(records[id])
    except KeyError:
        return {"message": f"Record with this id does not exist: <{id}>"}, 404


@app.get("/records")
def get_records():
    record_id = request.args.get("record_id")
    category_id = request.args.get("category_id")
    if not record_id and not category_id:
        return {
            "error": "At least one of the following query parameters should be present: [record_id, category_id]"}, 404
    return record_schema.dump(list(filter(lambda r: not category_id or r.category_id == category_id,
                                          filter(lambda r: not record_id or r.record_id == record_id,
                                                 records.values())))
                              , many=True)


@app.delete("/record/<id>")
def delete_record(id):
    try:
        return record_schema.dump(records.pop(id))
    except KeyError:
        return {"message": f"Record with this id does not exist: <{id}>"}, 404


@app.post("/record")
def create_record():
    record_data = request.get_json()
    if not record_data: return {"message": "No input data provided"}, 404
    try:
        record = record_schema.load(record_data)
    except ValidationError as err:
        return err.messages, 422

    if record.category_id not in categories: return {"message": f"Category with this id does not exist: {record.category_id}"}, 404
    if record.user_id not in users: return {"message": f"User with this id does not exist: {record.user_id}"}, 404

    category = categories[record.category_id]
    if category.owner_id and category.owner_id != record.user_id:
        return {"message": f"Category is not public and does not belong to the specified user. Category: {category.id}, User ({record.user_id}) != Owner({category.owner_id})"}
    records[record.id] = record
    return record_schema.dump(record)
