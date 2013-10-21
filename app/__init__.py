import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')

from app import views

