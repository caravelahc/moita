import errno
import sys

import config
import flask
import pymongo
import pymongo.errors

app = flask.Flask(__name__)
app.config.from_object(config)

try:
    connection = pymongo.MongoClient()
except pymongo.errors.ConnectionFailure:  # pragma: no cover
    print('Error %d: connection to the database refused.' % errno.ECONNREFUSED,
          file=sys.stderr)
    sys.exit(errno.ECONNREFUSED)

database = connection[app.config['DATABASE']]
timetables = database.timetables


@app.route('/load/<identifier>', methods=['GET'])
def load_timetable(identifier):
    payload = timetables.find_one(identifier)

    if payload is None:
        flask.abort(404)

    del payload['_id']
    return flask.jsonify(**payload), 200


@app.route('/store/<identifier>', methods=['PUT'])
def store_timetable(identifier):
    data = flask.request.form.to_dict()
    data['_id'] = identifier

    timetables.save(data)

    return '', 204