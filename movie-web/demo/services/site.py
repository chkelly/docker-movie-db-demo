import os
import json
import flask
import requests
from flask import render_template, url_for, request

app = flask.Flask(__name__)

MOVIE_API_URL = os.environ.get('MOVIE_API_URL', None)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search')
def search():
  year = request.args.get('year')
  request_data = {'year':year}

  response = requests.post(MOVIE_API_URL + '/movies/by/year', json = request_data)

  data = response.json()
  return render_template('results.html', movies=data)
