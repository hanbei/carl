# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_bootstrap import Bootstrap

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://postgres:passwd@172.17.0.2:5432/carl')
DEBUG = os.environ.get('DEBUG', True)
SECRET_KEY = os.environ.get('SECRET_KEY', 'development key')
USERNAME = os.environ.get('USERNAME', 'admin')
PASSWORD = os.environ.get('PASSWORD', 'admin')

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

from carl.navigation import nav

nav.init_app(app)

import carl.views
