import config
import errno
import sys

import boto
import boto.s3.connection as s3connection
import boto.s3.key as s3key
import flask
import json

app = flask.Flask(__name__)
app.config.from_object(config)

map = flask.Blueprint('moita', __name__)

s3 = s3connection.S3Connection()
bucket = s3.get_bucket(app.config['AWS_BUCKET_NAME'])


def download(filename):
    key = s3key.Key(bucket)
    key.key = '%s.json' % (filename,)
    filedata = key.get_contents_as_string()
    try:
        return json.loads(filedata.decode('utf-8'))
    except UnicodeError:
        return None


def upload(filename, filedata):
    key = s3key.Key(bucket)
    key.key = '%s.json' % (filename,)
    key.set_contents_from_string(json.dumps(filedata), headers={
            'Content-Type': 'application/json',
    })
    return key


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
