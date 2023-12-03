import datetime
import random

from webapp.model import User, Category, Record


def generate_users(names):
    for name in names:
        new_user = User(name)
        yield new_user.id, new_user


def generate_categories(categories):
    for category in categories:
        new_category = Category(category)
        yield new_category.id, new_category


def generate_records(users, categories):
    for user in list(users):
        for category in list(categories):
            # if random.choice([True, False]): continue  # generate or not generate randomly for each user and category
            record = generate_record(category, user)
            yield record.id, record


def generate_record(category: Category, user: User):
    sum = random.randint(0, 500)
    created = datetime.datetime(2023, 12,
                                random.randint(1, 31),
                                random.randint(0, 23),
                                random.randint(0, 59),
                                0)
    record = Record(user.id, category.id, created=created, sum=sum)
    return record
