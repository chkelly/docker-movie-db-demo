import os
import json
import flask
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from flask import request

app = flask.Flask(__name__)

dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL', None)

if dynamodb_endpoint_url:
  DYNAMODB = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
  DYNAMODB = boto3.resource('dynamodb')

table = os.environ.get('DYNAMODB_TABLE_NAME', 'Movies')

TABLE=DYNAMODB.Table(table)

@app.route('/')
def index():
  return 'Hello World! This is a test of the instance editing ability.'

@app.route('/movies/by/year', methods=['POST'])
def movies_by_year():
  request_data = request.get_json()
  print request_data
  year = int(request_data['year'])

  response = TABLE.query(
    KeyConditionExpression=Key('year').eq(year)
  )
  
  data = []
  for i in response['Items']:

    # convert decimals from dynamo
    i['info']['rating'] = float(i['info']['rating'])
    i['info']['rank'] = int(i['info']['rank'])
    i['info']['running_time_secs'] = int(i['info']['running_time_secs'])
    i['year'] = int(i['year'])

    data.append(i)

  return json.dumps(data)
