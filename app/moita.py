import config
import errno
import sys

import flask

app = flask.Flask(__name__)
app.config.from_object(config)

map = flask.Blueprint('moita', __name__)


@map.route('/load/<identifier>', methods=['GET'])
def load_timetable(identifier):
    payload = download(identifier)

    if payload is None:
        flask.abort(404)

    return flask.jsonify(**payload), 200


@map.route('/store/<identifier>', methods=['PUT'])
def store_timetable(identifier):
    data = flask.request.form.to_dict()
    upload(identifier, data)

    return '', 204


app.register_blueprint(map, url_prefix=app.config.get('APPLICATION_ROOT'))


def create_app(**kwargs):
    app.config.update(kwargs)

    return app
