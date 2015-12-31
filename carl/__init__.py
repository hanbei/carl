from flask import Flask
from flask_bootstrap import Bootstrap

DATABASE_URL = 'postgres://postgres:passwd@172.17.0.2:5432/carl'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(__name__)
app.config.from_envvar('DATABASE_URL', silent=True)

import carl.views
