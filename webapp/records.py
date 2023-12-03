import dataclasses

from flask import request

from webapp import app
from webapp.data import records
from webapp.model import Record


@app.get("/record/<id>")
def get_record(id):
    return dataclasses.asdict(records[id])


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
