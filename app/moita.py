import errno
import sys

import flask
import pymongo
import pymongo.errors

try:
    connection = pymongo.MongoClient()
except pymongo.errors.ConnectionFailure:  # pragma: no cover
    print('Error %d: connection to the database refused.' % errno.ECONNREFUSED,
          file=sys.stderr)
    sys.exit(errno.ECONNREFUSED)

map = flask.Blueprint('moita', __name__)


@map.route('/load/<identifier>', methods=['GET'])
def load_timetable(identifier):
    payload = connection[
        flask.current_app.config['DATABASE']].timetables.find_one(identifier)

    if payload is None:
        flask.abort(404)

    del payload['_id']
    return flask.jsonify(**payload), 200


@map.route('/store/<identifier>', methods=['PUT'])
def store_timetable(identifier):
    data = flask.request.form.to_dict()
    data['_id'] = identifier

    connection[flask.current_app.config['DATABASE']].timetables.save(data)

    return '', 204


def create_app(**kwargs):
    app = flask.Flask(__name__)

    import config

    app.config.from_object(config)
    app.config.update(kwargs)

    app.register_blueprint(map, url_prefix=app.config.get('APPLICATION_ROOT'))

    return app