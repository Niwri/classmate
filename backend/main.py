import os

from flask import Flask

from firebase_api import firebase_api

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


def register_blueprints(app):
    app.register_blueprint(firebase_api, url_prefix='/api')

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)