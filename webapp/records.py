import dataclasses
import datetime

from flask import request

from webapp import app
from webapp.data import records
from webapp.model import Record


@app.get("/record/<id>")
def get_record(id):
    return dataclasses.asdict(records[id])


@app.get("/records")
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    if not user_id and not category_id:
        return {
            "error": "At least one of the following query parameters should be present: [user_id, category_id]"}, 404
    return list(filter(lambda r: not category_id or r.category_id == category_id,
                       filter(lambda r: not user_id or r.user_id == user_id,
                              records.values())))


@app.delete("/record/<id>")
def delete_record(id):
    return dataclasses.asdict(records.pop(id))


@app.post("/record")
def create_record():
    record_data = request.get_json()
    record = Record(**record_data, created=str(datetime.datetime.now()))
    records[record.id] = record
    return dataclasses.asdict(record)
