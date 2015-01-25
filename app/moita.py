import config
import flask
import pymongo

app = flask.Flask(__name__)
app.config.from_object(config)

connection = pymongo.MongoClient()
database = connection[app.config['DATABASE']]
timetables = database.timetables