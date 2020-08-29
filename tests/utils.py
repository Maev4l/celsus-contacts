import json
import os
import psycopg2


def make_mock_event(subject, body=None):
    mock_event = {
        'userId': subject,
        'payload': body
    }
    return mock_event


def make_mock_message(message, reply_address=None):
    record = {
        'messageId': '0',
        'body': json.dumps(message),
        'messageAttributes': {}
    }

    if reply_address is not None:
        record['messageAttributes'] = {
            'replyAddress': {
                'stringValue': reply_address
            }
        }

    return {
        'Records': [record]
    }


def getConnection():
    hostname = os.environ['PGHOST']
    port = os.environ['PGPORT']
    database = os.environ['PGDATABASE']
    user = os.environ['PGUSER']
    password = os.environ['PGPASSWORD']

    connection = psycopg2.connect(
        host=f'{hostname}',
        port=f'{port}',
        database=f'{database}',
        user=f'{user}',
        password=f'{password}'
    )

    return connection
