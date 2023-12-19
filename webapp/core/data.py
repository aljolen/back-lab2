from webapp.core.utils import generate_users, generate_categories, generate_user_categories, generate_records

users = dict(generate_users(["Alpha", "Beta", "Gamma", "Delta"]))
general_categories = dict(generate_categories(["Tech", "Clothes", "Laptops"]))
user_categories = dict(generate_user_categories(users.values(), ["Tables", "Mugs", "Headphones", "Birthday"]))
categories = general_categories | user_categories
records = dict(generate_records(users.values(), categories.values()))