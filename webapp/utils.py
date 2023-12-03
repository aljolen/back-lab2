import uuid


def generate_users(names):
    for name in names:
        user_id = uuid.uuid4().hex
        yield user_id, {"name": name, "id": user_id}
