# Transforme app en package python.

from flask import Flask

app = Flask(__name__)

from .views import *
