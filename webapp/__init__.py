from flask import Flask

app = Flask(__name__)

import webapp.users
import webapp.categories
import webapp.records
