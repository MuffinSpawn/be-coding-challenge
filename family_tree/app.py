from flask import Flask
import flask_cors

from family_tree.database import Database
from family_tree.views import health_check, person, relationship

cors = flask_cors.CORS()


def create_app(config=None, db_path=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    cors.init_app(app)

    app.config['db'] = Database(path=db_path)

    app.register_blueprint(health_check.blueprint, url_prefix='/api')
    app.register_blueprint(person.blueprint, url_prefix='/api')
    app.register_blueprint(relationship.blueprint, url_prefix='/api')
    # print(app.url_map)

    return app
