import config
import flask
import pymongo

app = flask.Flask(__name__)
app.config.from_object(config)

db = pymongo.MongoClient()