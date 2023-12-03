import dataclasses

from flask import request

from webapp import app
from webapp.data import records
from webapp.model import Record


@app.get("/record/<id>")
def get_record(id):
    return dataclasses.asdict(records[id])


@app.get("/record")
def get_record_filter():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    if user_id is None and category_id is None:
        return {
            "error": "At least one of the following query parameters should be present: [user_id, category_id]"}, 404
    return list(filter(lambda r: category_id is None or r.category_id == category_id,
                       filter(lambda r: user_id is None or r.user_id == user_id,
                              records.values())))


@app.delete("/record/<id>")
def delete_record(id):
    return dataclasses.asdict(records.pop(id))


@app.post("/record")
def create_record():
    record_data = request.get_json()
    record = Record(**record_data)
    records[record.id] = record
    return dataclasses.asdict(record)


@app.get("/records")
def get_records():
    return list(records.values())
