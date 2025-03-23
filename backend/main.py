import os

from flask import Flask
from flask_cors import CORS
from homework_api import homework_api
from classroom_api import classroom_api

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def register_blueprints(app):
    app.register_blueprint(homework_api, url_prefix='/homework')
    app.register_blueprint(classroom_api, url_prefix='/classroom')

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)