import importlib
import os
import secrets
from pathlib import Path
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_mongoengine import MongoEngine

from errors import page_not_found

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

app.config.update(
    TESTING=True,
    JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
)
app.config['TESTING'] = True
app.secret_key = secrets.token_urlsafe(16)
app.register_error_handler(404, page_not_found)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'myapp',
    'host': 'mongodb+srv://Admin:trudne_haslo.123@cluster0.c1l5u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
}

db = MongoEngine(app)

module_list_model = []
for package_model in os.listdir(os.path.join(Path(__file__).resolve().parent, 'model')):
    module = importlib.import_module('model.' + package_model)
    if hasattr(module, 'MOD_NAME'):
        module_list_model.append(module.MOD_NAME)

module_list_control = []
for package in os.listdir(os.path.join(Path(__file__).resolve().parent, 'control')):
    module = importlib.import_module('control.' + package)
    if hasattr(module, 'IGNORED') and hasattr(module, 'api') and hasattr(module, 'MOD_NAME'):
        if not module.IGNORED:
            app.register_blueprint(module.api, url_prefix='/' + module.MOD_NAME)
            module_list_control.append(module.MOD_NAME)



if __name__ == '__main__':
    app.run()
