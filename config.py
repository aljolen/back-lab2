import os

FLASK_DEBUG = True
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"