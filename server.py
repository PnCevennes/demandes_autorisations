import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_compress import Compress

from app.env import db

from config import config

class ReverseProxied(object):

    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


print(config.URL_APPLICATION)
app = Flask(
    __name__,
    template_folder="templates",
    static_folder='static'
)

app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=config.URL_APPLICATION)

app.config.from_pyfile('config/config.py')

db.init_app(app)

with app.app_context():
    from app import routes
    app.register_blueprint(routes.route, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=False, port=5555)
