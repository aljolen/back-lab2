from webapp.utils import generate_users, generate_categories, generate_records

users = dict(generate_users(["Alpha", "Beta", "Gamma", "Delta"]))
categories = dict(generate_categories(["Tech", "Clothes", "Laptops"]))
records = dict(generate_records(users.values(), categories.values()))