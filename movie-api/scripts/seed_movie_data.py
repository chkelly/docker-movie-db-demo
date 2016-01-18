from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import sys, os
from boto3.dynamodb.conditions import Key, Attr

def main():
  dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL', None)

  if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
  else:
    dynamodb = boto3.resource('dynamodb')

  table = os.environ.get('DYNAMODB_TABLE_NAME', 'Movies')

  if table in (t.name for t in dynamodb.tables.all()):
    table = dynamodb.Table(table)
  else:
    table = dynamodb.create_table(
      TableName='Movies',
      KeySchema=[
          {
              'AttributeName': 'year',
              'KeyType': 'HASH'  #Partition key
          },
          {
              'AttributeName': 'title',
              'KeyType': 'RANGE'  #Sort key
          }
      ],
      AttributeDefinitions=[
          {
              'AttributeName': 'year',
              'AttributeType': 'N'
          },
          {
              'AttributeName': 'title',
              'AttributeType': 'S'
          },

      ],
      ProvisionedThroughput={
          'ReadCapacityUnits': 10,
          'WriteCapacityUnits': 10
      }
    )

  print("Table status:", table.table_status)

  with open(os.path.dirname(os.path.realpath(__file__)) + "/../data/moviedata.json") as json_file:
      movies = json.load(json_file, parse_float = decimal.Decimal)
      count = 0
      for movie in movies:
          year = int(movie['year'])
          title = movie['title']
          info = movie['info']

          print("Adding movie:", year, title)

          table.put_item(
             Item={
                 'year': year,
                 'title': title,
                 'info': info,
              }
          )
          count += 1
          
  print("Number of seeded items:", count)

if __name__ == '__main__':
  main()
