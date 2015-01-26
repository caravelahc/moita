import config
import errno
import flask
import pymongo
import pymongo.errors
import sys

app = flask.Flask(__name__)
app.config.from_object(config)

try:
    connection = pymongo.MongoClient()
except pymongo.errors.ConnectionFailure:
    print('Error %d: connection to the database refused.' % errno.ECONNREFUSED, file=sys.stderr)
    sys.exit(errno.ECONNREFUSED)


database = connection[app.config['DATABASE']]
timetables = database.timetables