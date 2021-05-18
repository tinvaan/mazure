
from gzip import compress
from json import dumps, loads
from flask import current_app as app
from flask_mongoengine import MongoEngine


store = MongoEngine(app._get_current_object())
