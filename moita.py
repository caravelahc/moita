import os
import flask
import sqlite3

from dotenv import load_dotenv
from textwrap import dedent
from flask_cors import CORS


def initialize_db():
    db = sqlite3.connect("matrufsc.db")
    db.execute(
        dedent(
            """\
            create table if not exists schedules (
                id text primary key,
                json_data text
            );
        """
        )
    )


map = flask.Blueprint("moita", __name__)


@map.route("/")
def ok():
    return "OK"


@map.route("/load/<identifier>", methods=["GET"])
def load_timetable(identifier):
    with sqlite3.connect("matrufsc.db") as db:
        query = dedent(
            """\
            select json_data
            from schedules
            where id = ?
        """
        )
        result, *_ = db.execute(query, (identifier,))

    return result[0], 200


@map.route("/store/<identifier>", methods=["PUT"])
def store_timetable(identifier):
    data = flask.request.get_json()

    with sqlite3.connect("matrufsc.db") as db:
        db.execute(
            dedent(
                """\
                insert or replace into schedules(id, json_data)
                values (?, ?)
            """
            ),
            (identifier, str(data)),
        )

    return "", 204


def create_app(**kwargs):
    load_dotenv(".env")
    app = flask.Flask(__name__)
    app.register_blueprint(map, url_prefix="/")
    initialize_db()
    return app


if __name__ == "__main__":
    app = create_app()
    origins = os.getenv("CORS_ACCEPTED_ORIGIN")
    cors = CORS(
        app,
        resources={r"/*": {"origins": origins}},
    )
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(os.getenv("APP_HOST", "localhost"), os.getenv("APP_PORT", "8001"), debug)
