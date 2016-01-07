import os
import json
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  return 'Hello World! This is a test of the instance editing ability.'
